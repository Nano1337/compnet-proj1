#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  Modified: Fall 2022 (for Computer Networking course)
#
#  Purpose: demonstrate serialization of a user-defined data structure using
#  FlatBuffers
#
#  Here our custom message format comprises a sequence number, a timestamp, a name,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us) 

# The different packages we need in this Python driver code
import os
import sys
import time  # needed for timing measurements and sleep

import random  # random number generator
import argparse  # argument parser

## the following are our files
from custom_msg import CustomMessage  # our custom message in native format
import serialize as sz  # this is from the file serialize.py in the same directory

##################################
#        Driver program
##################################


def driver(name, iters, vec_len):
    print("Driver program: Name = {}, Num Iters = {}, Vector len = {}".format(name, iters, vec_len))
    
    for i in range(iters):
        # for every iteration, let us fill up our custom message
        cm = CustomMessage()  # create a new instance for each iteration

        cm.type = "ORDER"        

        # Generate random values for Veggies
        veggies = {
            'tomato': random.uniform(0, 5),
            'cucumber': random.uniform(0, 5),
            'lettuce': random.uniform(0, 5),
            'broccoli': random.uniform(0, 5),
            'spinach': random.uniform(0, 5),
            'carrots': random.uniform(0, 5)
        }

        # Generate random values for DrinksCans
        drinks_cans = {
            'coke': random.randint(1, 5),
            'beer': random.randint(1, 5),
            'lemonade': random.randint(1, 5)
        }

        # Generate random values for DrinksBottles
        drinks_bottles = {
            'sprite': random.randint(1, 5),
            'gingerale': random.randint(1, 5),
            'water': random.randint(1, 5)
        }

        # Aggregate Drinks
        drinks = {
            'cans': drinks_cans,
            'bottles': drinks_bottles
        }

        # Generate random values for Milk
        milk = [{
            'type': random.choice(['ONE_PERCENT', 'TWO_PERCENT', 'FAT_FREE', 'WHOLE', 'ALMOND', 'CASHEW', 'OAT']),
            'quantity': random.uniform(0, 5)
        }]

        # Generate random values for Bread
        bread = [{
            'type': random.choice(['WHOLE_WHEAT', 'PUMPERNICKEL', 'RYE']),
            'quantity': random.uniform(0, 5)
        }]

        # Generate random values for Meat
        meat = [{
            'type': random.choice(['BEEF', 'CHICKEN', 'PORK', 'TURKEY']),
            'quantity': random.uniform(0, 5)
        }]

        # Combine all into Order
        cm.order = {
            'veggies': veggies,
            'drinks': drinks,
            'milk': milk,
            'bread': bread,
            'meat': meat
        }

        print(cm)

        
        print("-----Iteration: {} contents of message before serializing ----------".format(i))
        cm.dump()

        # serialize the message
        print("serialize the message")
        start_time = time.time()
        buf = sz.serialize(cm)
        end_time = time.time()
        print("Serialization took {} secs".format(end_time - start_time))

        # deserialize and inspect the result
        print("deserialize the message")
        start_time = time.time()
        cm = sz.deserialize(buf)
        end_time = time.time()
        print("Deserialization took {} secs".format(end_time - start_time))

        print("------ contents of message after deserializing ----------")
        cm.dump()

        time.sleep(0.050)  # 50 msec


##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()

    # add optional arguments
    parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations to run (default: 10)")
    parser.add_argument ("-l", "--veclen", type=int, default=20, help="Length of the vector field (default: 20; contents are irrelevant)")
    parser.add_argument ("-n", "--name", default="FlatBuffer Local Demo", help="Name to include in each message")
    # parse the args
    args = parser.parse_args ()

    return args
    
#------------------------------------------
# main function
def main ():
    """ Main program """

    print("Demo program for Flatbuffer serialization/deserialization")

    # first parse the command line args
    parsed_args = parseCmdLineArgs ()
    
   # start the driver code
    driver (parsed_args.name, parsed_args.iters, parsed_args.veclen)

#----------------------------------------------
if __name__ == '__main__':
    main ()
