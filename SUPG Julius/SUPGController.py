#SUPG Controller Class

import math
from sNeuron import sNeuron
import numpy as np

# radius, offset, step_height, phase, duty_factor
tripod_gait = [	0.15, 0, 0.05, 0.5, 0.5, # leg 1
				0.15, 0, 0.05, 0.0, 0.5, # leg 2
				0.15, 0, 0.05, 0.5, 0.5, # leg 3
				0.15, 0, 0.05, 0.0, 0.5, # leg 4
				0.15, 0, 0.05, 0.5, 0.5, # leg 5
				0.15, 0, 0.05, 0.0, 0.5] # leg 6

class SUPGController:

    def __init__(self, cppn, params=tripod_gait, body_height=0.4, period=1.0, velocity=0.46, crab_angle=0.0, dt=1/240):

        # link lengths
        self.l_1 = 0.05317
        self.l_2 = 0.10188
        self.l_3 = 0.14735

        self.dt = dt
        self.period = period
        self.velocity = velocity
        self.crab_angle = crab_angle
        self.body_height = body_height

        self.wavelength = 100 # SUPG-Wavelength
        self.supgOutputs = [] #Cache CPPN outputs
        self.cppn = cppn
        self.neuronList = []
        self.firstStep = False
        self.setCoordinates()
        self.initialOutputs = []

        for i in range(6):
            self.initialOutputs.append(0)
            self.initialOutputs.append(0.8994219)
            self.initialOutputs.append(-1.487756)

    def setCoordinates(self):
        #create nodes
        for i in range(12):
            self.neuronList.append(sNeuron(i))
        
        #neurons are ordered l0s1, l0s2, l1s1, l1s2... (l0 = leg 0 && s1 = servo 1)
        #need to experiment with different servo numbers. i.e., 3 instead of 2
        #set co-ordinates in substrate
        for neuron in self.neuronList:
            #set y-axis
            if(neuron.ID() in [0,1,10,11]):
                neuron.setYPos(0.5)

            elif(neuron.ID() in [2,3,8,9]):
                neuron.setYPos(0)
            
            elif(neuron.ID() in [4,5,6,7]):
                neuron.setYPos(-0.5)

            #set x-axis
            if (neuron.ID() >= 0 and neuron.ID() < 6):
                if(neuron.ID() % 2 == 0):
                    neuron.setXPos(0.4)
                else:
                    neuron.setXPos(0.6)

            elif (neuron.ID() >= 6 and neuron.ID() < 12):
                if(neuron.ID() % 2 == 0):
                    neuron.setXPos(-0.6)
                else:
                    neuron.setXPos(-0.4)

    #offsets are used to ensure the robot does not fire all legs at once on the initial angle request
    #offsets are discarded after 1st step
    def getOffset(self, neuron):
        #potentially use compression value for x position
        offset = 0
        inputs = []
        inputs.append(0)
        inputs.append(neuron.getYPos()/50) #uses y angle to ensure all servos on same leg move at same time
        inputs.append(0)
    
        activation = self.cppn.activate(inputs)
        offset = (activation[1] + 1)
      
        if (offset >= 0 and offset <=1 ):
            return False
        else:
            return True
        
    ##return output of individual 
    def getSUPGActivation(self, neuron):
        coordinates = []
        coordinates.append(neuron.getXPos())
        coordinates.append(neuron.getYPos())
        coordinates.append(neuron.getTimeCounter() / self.wavelength) 

        activation = self.cppn.activate(coordinates)

        # with the SUPG architecture, we need the outputs to be normalized between 0 and 1
        # because the CPPN uses bipolar sigmoid for all outputs, which increases the range to -1, 1
        output = (activation[0]+1)/2

        return output

    #update timer --> use after CPPN input has being called
    # for future: map triggers to each leg --> wraps entire def in an IF
    def update(self):
        for neuron in self.neuronList:
            if neuron.getTimeCounter() >= 1:
                neuron.setTimeCounter(0)
            elif neuron.getTimeCounter() >=0 and neuron.getTimeCounter() < 1:
                neuron.setTimeCounter((neuron.getTimeCounter() + 1) % self.wavelength)
    
    def IMU_feedback(self, measured_attitude):
            return

    #reshape output to be within correct scale for each joint
    def reshapeServoOutput(self, neuron,  output):
            #coxa
            NewValue = 0
            if(neuron.ID() % 2 == 0):
                OldRange = (1 - 0)  
                NewRange = (1.74533 - (-1.74533))  
                NewValue = (((output - 0) * NewRange) / OldRange) + (-1.74533)
            #femur
            else:
                OldRange = (1 - 0)  
                NewRange = (2.26893 - (-2.61799))  
                NewValue = (((output - 0) * NewRange) / OldRange) + (-2.61799)

            return NewValue
            
    #query each supg for output, cache output in an array, then output angles to correct joints
    def joint_angles(self, t):

        outputs = []

        if t == 0:
            return self.initialOutputs
        else:
            #set timer to offset to kickstart legs/avoid pronk
            #legs where offset == true , remain at T zero
            if(self.firstStep == False):
                for neuron in self.neuronList:
                    if self.getOffset(neuron) == True: #has an offset
                        neuron.setTimeCounter(1.1) # set value outside of reference range. i.e., won't fire on first time step
                self.firstStep = True

         #only need SUPG output for neurons with timer above zero... i.e, legs with offset outside of value wont move on initial time step
            for neuron in self.neuronList:
                if(neuron.getTimeCounter() >=0 and neuron.getTimeCounter() <=1):
                    #rescale output within range for each type of joint
                    output = self.reshapeServoOutput(neuron, self.getSUPGActivation(neuron))
                    outputs.append(output)
                else:
                    #if leg is not ready to move due to offset, keep value at stationary gait value.
                    if neuron.ID() % 2 == 0:
                        outputs.append(0)
                    else:
                        outputs.append(0.8994219)

            self.update()

            self.supgOutputs = outputs # caching outputs for later use when coupling            

            #adding tibia output, which remains constant
            i = 2
            while i <= len(outputs):
                outputs.insert(i, -1.487756)
                i += (2+1)

            return np.array(outputs)