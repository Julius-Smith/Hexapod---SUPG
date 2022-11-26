import math
import pickle
import neat
import visualize
import neat.nn
import numpy as np
import multiprocessing
import os
import sys
import visualize as vz
import shutil
##from hexapod.controllers.hyperNEATController import Controller, reshape, stationary
from SUPGController import SUPGController
from mailer.hexapod.simulator import Simulator
import pymap_elites.map_elites.common as cm
import pymap_elites.map_elites.cvt as cvt_map_elites
from neat.reporting import ReporterSet

"""
A script to produce the HyperNEAT maps
The script takes two command line arguments:
1) The size of the map to be tested
2) The run/map number
"""
#configure neat for the SUPG CPPN
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     r'config_SUPG')  #C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\JSUPG\config_SUPG

# radius, offset, step_height, phase, duty_factor
tripod_gait = [	0.15, 0, 0.05, 0.5, 0.5, # leg 1
				0.15, 0, 0.05, 0.0, 0.5, # leg 2
				0.15, 0, 0.05, 0.5, 0.5, # leg 3
				0.15, 0, 0.05, 0.0, 0.5, # leg 4
				0.15, 0, 0.05, 0.5, 0.5, # leg 5
				0.15, 0, 0.05, 0.0, 0.5] # leg 6

# Fitness function that returns fitness and behavioural descriptor

def evaluate_gait(x, duration=5):
    cppn = neat.nn.FeedForwardNetwork.create(x, config)
    # Reset net

    leg_params = np.array(tripod_gait).reshape(6, 5)

    try:
        controller = SUPGController(cppn, [] )
    except:
        return 0, np.zeros(6)
    # Initialise Simulator
    simulator = Simulator(controller=controller, visualiser=False, collision_fatal=True)
    # Step in simulator
    contact_sequence = np.full((6, 0), False)
    for t in np.arange(0, duration, step=simulator.dt):
        try:
            simulator.step()
        except RuntimeError as collision:
            fitness = 0, np.zeros(6)
        contact_sequence = np.append(contact_sequence, simulator.supporting_legs().reshape(-1, 1), axis=1)
    fitness = simulator.base_pos()[0]  # distance travelled along x axis
    descriptor = np.nan_to_num(np.sum(contact_sequence, axis=1) / np.size(contact_sequence, axis=1), nan=0.0,
                               posinf=0.0, neginf=0.0)
    # Terminate Simulator
    simulator.terminate()
    # print(difference)
    # fitness = difference
    # Assign fitness to genome
    x.fitness = fitness
    return fitness, descriptor

# Method to load in initial high performing genomes
def load_genomes(num=200):
    reporters = ReporterSet()
    stagnation = config.stagnation_type(config.stagnation_config, reporters)
    reproduction = config.reproduction_type(config.reproduction_config, reporters, stagnation)

    genomes = reproduction.create_new(config.genome_type, config.genome_config, num)
    print(type(genomes))
    print(type(list(genomes.values())))
    return list(genomes.values())

if __name__ == '__main__':
    mapSize = int(sys.argv[1])
    runNum = (sys.argv[2])
    # Map Elites paramters
    params = \
        {
            # more of this -> higher-quality CVT
            "cvt_samples": 1000000,
            # we evaluate in batches to parallelise
            "batch_size": 2390,
            # proportion of niches to be filled before starting (400)
            "random_init": 0.01,
            # batch for random initialization
            "random_init_batch": 2390,
            # when to write results (one generation = one batch)
            "dump_period": 1e6,   # Change that
            # do we use several cores?
            "parallel": True,
            # do we cache the result of CVT and reuse?
            "cvt_use_cache": True,
            # min/max of parameters
            "min": 0,
            "max": 1,
        }

    # Used when starting from seeded genomes.
    #genomes = load_genomes()

    # Used when loading in checkpointed values
    filename = 'mapElitesOutput/'+ runNum+'_20000archive/archive_genome6001448.pkl'
    archive_load_file_name = 'mapElitesOutput/'+runNum+'_20000archive/archive6001448.dat'
    with open(filename, 'rb') as f:
        genomes = pickle.load(f)
        print(len(genomes))

    if not os.path.exists("mapElitesOutput/" + runNum + "_" + str(mapSize)):
        os.mkdir("mapElitesOutput/" + runNum + "_" + str(mapSize))
    if not os.path.exists("mapElitesOutput/" + runNum + "_" + str(mapSize) + "archive"):
        os.mkdir("mapElitesOutput/" + runNum + "_" + str(mapSize) + "archive")

    # Used when initially loading in
    archive = cvt_map_elites.compute(6, genomes, evaluate_gait, n_niches = mapSize, max_evals=10e6,
                             log_file=open('mapElitesOutput/' + runNum + "_" + str(mapSize) + '/log.dat', 'w'), archive_file='mapElitesOutput/' + runNum + "_" + str(mapSize) + "archive" + '/archive',
                             params=params, variation_operator=cm.neatMutation)

    # Used when loading from archived files
    # archive = cvt_map_elites.compute(6, genomes, evaluate_gait, n_niches=mapSize, max_evals=8e6,
    #                                  log_file=open('mapElitesOutput/' + runNum + "_" + str(mapSize) + '/log.dat', 'a'), archive_file='mapElitesOutput/' + runNum + "_" + str(mapSize) + "archive" + '/archive',
    #                                  archive_load_file=archive_load_file_name, params=params, start_index=6001448,
    #                                  variation_operator=cm.neatMutation)