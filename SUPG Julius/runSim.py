#SUPG Controller Class
from mailer.hexapod.simulator import Simulator
from SUPGController import SUPGController
import neat
import neat.nn
import numpy as np
import pickle
import multiprocessing

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     r'C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\SUPG Julius\config_SUPG')  #C:\Users\Dell\Documents\University\Unversity2022\Thesis\Hexapod Code\Hexapod---SUPG\SUPG Julius\config_SUPG
def bipolarSig(x):
    return (1 - np.exp(-x)) / (1 + np.exp(-x))

config.genome_config.add_activation('bisig', bipolarSig)

#read in pickl
with open("SUPG_xor_cppn.pkl", 'rb') as f:
    CPPN = pickle.load(f)

#set up final controller and feed into sim
    controller = SUPGController(CPPN)
    simulator = Simulator(controller, follow=True, visualiser=True, collision_fatal=False, failed_legs=[])

    # run indefinitely
    while True:
        simulator.step()
