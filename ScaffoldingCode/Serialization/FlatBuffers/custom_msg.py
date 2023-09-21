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
        print("    Dispenser: {}".format(self.health.get('dispenser')))
        print("    Icemaker: {}".format(self.health.get('icemaker')))
        print("    Lightbulb: {}".format(self.health.get('lightbulb')))
        print("    Fridge Temperature: {}".format(self.health.get('fridge_temp')))
        print("    Freezer Temperature: {}".format(self.health.get('freezer_temp')))
        print("    Sensor Status: {}".format(self.health.get('sensor_status')))
    
    elif self.type == "RESPONSE" and self.response:
        #FIXME: not the right way to print out
        print("  Response Details:")
        print("    Code: {}".format(self.response.get('code')))
        print("    Contents: {}".format(self.response.get('contents')))
