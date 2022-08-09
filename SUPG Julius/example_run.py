from mailer.hexapod.simulator import Simulator
from SUPGController import SUPGController
import neat
import neat.nn
import numpy as np
import pickle
import multiprocessing
import visualize

#configure neat for the SUPG CPPN
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     r'config_SUPG')  #C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\SUPG Julius\config_SUPG
def bipolarSig(x):
    return (1 - np.exp(-x)) / (1 + np.exp(-x))

config.genome_config.add_activation('bisig', bipolarSig)

# radius, offset, step_height, phase, duty_factor
tripod_gait = [	0.15, 0, 0.05, 0.5, 0.5, # leg 1
				0.15, 0, 0.05, 0.0, 0.5, # leg 2
				0.15, 0, 0.05, 0.5, 0.5, # leg 3
				0.15, 0, 0.05, 0.0, 0.5, # leg 4
				0.15, 0, 0.05, 0.5, 0.5, # leg 5
				0.15, 0, 0.05, 0.0, 0.5] # leg 6

#parralel implementation
def evaluate_gaitP(genome, config):
     # Create CPPN from Genome and configuration file
        #cppn = neat.nn.FeedForwardNetwork.create(genome, config)
        cppn = neat.nn.RecurrentNetwork.create(genome,config)
        
        
        leg_params = np.array(tripod_gait).reshape(6, 5)

        # Set up controller
        try:
           controller = SUPGController(cppn)
        except:
            
            return 0#, np.zeros(6)
            
        # Initialise Simulator
        simulator = Simulator(controller=controller, visualiser=False, collision_fatal=False)
        # Step in simulator
        for t in np.arange(0, 5, step=simulator.dt):
            try:
                simulator.step()
            except RuntimeError as collision:

                return 0#, np.zeros(6)

        fitness = simulator.base_pos()[0]  # distance travelled along x axis
        # Terminate Simulator
        simulator.terminate()

        return fitness

def evaluate_gait(genomes, config, duration=5):
    for genome_id, genome in genomes:
        # Create CPPN from Genome and configuration file
        cppn = neat.nn.FeedForwardNetwork.create(genome, config)
        
        
        leg_params = np.array(tripod_gait).reshape(6, 5)

        # Set up controller
        try:
           controller = SUPGController(cppn)
        except:
            return 0, np.zeros(6)
            
        # Initialise Simulator
        simulator = Simulator(controller=controller, visualiser=False, collision_fatal=False)
        # Step in simulator
        for t in np.arange(0, duration, step=simulator.dt):
            try:
                simulator.step()
            except RuntimeError as collision:
                fitness = 0, np.zeros(6)
        fitness = simulator.base_pos()[0]  # distance travelled along x axis
        # Terminate Simulator
        simulator.terminate()
        # Assign fitness to genome
        genome.fitness = fitness

def run(gens):
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(False))


    ## running in parallel
    pe =  neat.ParallelEvaluator(multiprocessing.cpu_count(), evaluate_gaitP)

    # Run until a solution is found.
    #winner = p.run(evaluate_gait, gens)

    winner = p.run(pe.evaluate, gens)
    return winner


if __name__ == "__main__":

    winner = run(25)
    
    #create network with winning genome
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    leg_params = np.array(tripod_gait).reshape(6, 5)



    with open('SUPG_xor_cppn5.pkl', 'wb') as output:
        pickle.dump(winner_net, output, pickle.HIGHEST_PROTOCOL)
        
    #visualize.draw_net(config, winner_net, filename="SUPG_xor_cppn_attemp1")
    #set up final controller and feed into sim
    #controller = SUPGController(winner_net)
    #simulator = Simulator(controller, follow=True, visualiser=True, collision_fatal=False, failed_legs=[])

    # run indefinitely
    #while True:
    #    simulator.step()