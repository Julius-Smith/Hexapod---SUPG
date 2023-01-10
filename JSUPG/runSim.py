#SUPG Controller Class
from mailer.hexapod.simulator import Simulator
from SUPGController import SUPGController
from BSUPGController import BSUPGController 
import neat
import neat.nn
import numpy as np
import pickle
import multiprocessing

#create NEAT configuration
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     r'C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\JSUPG\config_SUPG')  #C:\Users\Dell\Documents\Shared Folder\Hexapod---SUPG\SUPG Julius\config_SUPG


# radius, offset, step_height, phase, duty_factor
tripod_gait = [	0.15, 0, 0.05, 0.5, 0.5, # leg 1
				0.15, 0, 0.05, 0.0, 0.5, # leg 2
				0.15, 0, 0.05, 0.5, 0.5, # leg 3
				0.15, 0, 0.05, 0.0, 0.5, # leg 4
				0.15, 0, 0.05, 0.5, 0.5, # leg 5
				0.15, 0, 0.05, 0.0, 0.5] # leg 6

leg_params = np.array(tripod_gait).reshape(6, 5)


#read in pickl
with open(r"C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\JSUPG\Pickles\SUPG_xor_cppn_testECSUPG15.pkl", 'rb') as f:
    CPPN = pickle.load(f)

    #set up final controller and feed into sim
    #dictate which legs are broken
    broken =[] 
    brokenS = []
    controller = SUPGController(CPPN, broken)
    simulator = Simulator(controller, follow=True, visualiser=True, collision_fatal=False, failed_legs=brokenS)

    # run indefinitely
    while True:
        simulator.step()