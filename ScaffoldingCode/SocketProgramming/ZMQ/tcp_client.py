# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Code taken from ZeroMQ's sample code for the HelloWorld
# program, but modified to use REQ-REP sockets to showcase
# TCP. Plus, added other decorations like comments, print statements,
# argument parsing, etc.
#
# ZMQ is also offering a new CLIENT-SERVER pair of ZMQ sockets but
# these are still in draft form and are not properly supported. If you
# want to try, just replace REQ by CLIENT here (and correspondingly, in
# the tcp_server.py, replace REP by SERVER)
#
# Note: my default indentation is now set to 2 (in other snippets, it
# used to be 4)

# import the needed packages
import sys    # for system exception
import time   # for sleep
import argparse # for argument parsing
import zmq    # this package must be imported for ZMQ to work
sys.path.append('/home/roberthsheng/CN/compnet-proj1/ScaffoldingCode/Serialization/FlatBuffers/') # change this to the path of your serialize.py
import serialize as sz
from custom_msg import CustomMessage
import random

##################################
# Driver program
##################################
def driver (args):
  try:
    # every ZMQ session requires a context
    print ("Obtain the ZMQ context")
    context = zmq.Context ()   # returns a singleton object
  except zmq.ZMQError as err:
    print ("ZeroMQ Error: {}".format (err))
    return
  except:
    print ("Some exception occurred getting context {}".format (sys.exc_info()[0]))
    return

  try:
    # The socket concept in ZMQ is far more advanced than the traditional socket in
    # networking. Each socket we obtain from the context object must be of a certain
    # type. For TCP, we will use the REQ socket type (many other pairs are supported)
    # and this is to be used on the client side.
    socket = context.socket (zmq.REQ)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error obtaining context: {}".format (err))
    return
  except:
    print ("Some exception occurred getting REQ socket {}".format (sys.exc_info()[0]))
    return

  try:
    # as in a traditional socket, tell the system what IP addr and port are we
    # going to connect to. Here, we are using TCP sockets.
    connect_string = "tcp://" + args.addr + ":" + str (args.port)
    print ("TCP client will be connecting to {}".format (connect_string))
    socket.connect (connect_string)
  except zmq.ZMQError as err:
    print ("ZeroMQ Error connecting REQ socket: {}".format (err))
    socket.close ()
    return
  except:
    print ("Some exception occurred connecting REQ socket {}".format (sys.exc_info()[0]))
    socket.close ()
    return

  # since we are a client, we actively send something to the server
  print ("client sending Hello messages for specified num of iterations")
  for i in range (args.iters):
    try:
      cm = CustomMessage()  # create a new instance for each iteration

      cm.type = random.choice(['ORDER', 'HEALTH', 'RESPONSE'])     

      if cm.type == 'ORDER':

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
      
      elif cm.type == 'HEALTH':
          cm.health = {
              'dispenser': random.choice(['OPTIMAL', 'PARTIAL', 'BLOCKAGE']),
              'icemaker': random.randint(0, 5),
              'lightbulb': random.choice(['GOOD', 'BAD']),
              'fridge_temp': random.randint(0, 5),
              'freezer_temp': random.randint(0, 5),
              'sensor_status': random.choice(['GOOD', 'BAD']),
              'water_filter': random.choice(['GOOD', 'BAD'])
          }
      
      elif cm.type == 'RESPONSE':
          cm.response = {
              'code': random.choice(['OK', 'BAD_REQUEST']),
              'contents': random.choice(['OK', 'BAD_REQUEST'])
          }
      serialized_cm = sz.serialize(cm)
      socket.send (serialized_cm)
    except zmq.ZMQError as err:
      print ("ZeroMQ Error sending: {}".format (err))
      socket.close ()
      return
    except:
      print ("Some exception occurred receiving/sending {}".format (sys.exc_info()[0]))
      socket.close ()
      return

    try:
      # receive a reply
      print ("Waiting to receive")
      message = socket.recv()
      cm = sz.deserialize(message)
      print ("Received reply in iteration {} is:".format (i))
      cm.dump()
    except zmq.ZMQError as err:
      print ("ZeroMQ Error receiving: {}".format (err))
      socket.close ()
      return
    except:
      print ("Some exception occurred receiving/sending {}".format (sys.exc_info()[0]))
      socket.close ()
      return

##################################
# Command line parsing
##################################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-a", "--addr", default="127.0.0.1", help="IP Address to connect to (default: localhost i.e., 127.0.0.1)")
  parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations (default: 10")
  parser.add_argument ("-p", "--port", type=int, default=5555, help="Port that server is listening on (default: 5555)")
  args = parser.parse_args ()

  return args
    
#------------------------------------------
# main function
def main ():
  """ Main program """

  print("Demo program for TCP Client with ZeroMQ")

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()
    
  # start the driver code
  driver (parsed_args)

#----------------------------------------------
if __name__ == '__main__':
  # here we just print the version numbers
  print("Current libzmq version is %s" % zmq.zmq_version())
  print("Current pyzmq version is %s" % zmq.pyzmq_version())

  main ()
