# CS4283/5283: Computer Networks
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
#
# Purpose: Define a native representation of a custom message format
#          that will then undergo serialization/deserialization
#

from typing import List
from dataclasses import dataclass

@dataclass
class CustomMessage:
  """ Our message in native representation"""

  type = None # type of message
  order = None # order message
  health = None # health message
  response = None # response message

  def __init__ (self):
    pass
  
  def dump(self):
    print("Dumping contents of Custom Message")
    print("  Type: {}".format(self.type))
    
    if self.type == "ORDER" and self.order:
        print("  Order Details:")

        # print out all contents of the order
        for key, value in self.order.items():
            print("    {}: {}".format(key, value))

    elif self.type == "HEALTH" and self.health:
        #FIXME: not the right way to print out
        print("  Health Details:")
        for key, value in self.health.items():
            print("    {}: {}".format(key, value))
    
    elif self.type == "RESPONSE" and self.response:
        #FIXME: not the right way to print out
        print("  Response Details:")
        for key, value in self.response.items():
            print("    {}: {}".format(key, value))
