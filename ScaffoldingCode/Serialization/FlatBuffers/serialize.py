#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  (based on code developed for Distributed Systems course in Fall 2019)
#  Modified: Fall 2022 (changed packet name to not confuse with pub/sub Messages)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using flatbuffers
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import os
import sys

# this is needed to tell python where to find the flatbuffers package
# make sure to change this path to where you have compiled and installed
# flatbuffers.  If the python package is installed in your system wide files
# or virtualenv, then this may not be needed
sys.path.append(os.path.join (os.path.dirname(__file__), '/home/gokhale/Apps/flatbuffers/python'))
import flatbuffers    # this is the flatbuffers package we import
import time   # we need this get current time
import numpy as np  # to use in our vector field

import zmq   # we need this for additional constraints provided by the zmq serialization

from custom_msg import CustomMessage  # our custom message in native format
import CustomAppProto.Message as msg
from CustomAppProto.MessageType import MessageType
import CustomAppProto.Order as Order
import CustomAppProto.Health as Health
import CustomAppProto.Response as Response
import CustomAppProto.Milk as Milk
from CustomAppProto.MilkType import MilkType
import CustomAppProto.ResponseCode as ResponseCode
import CustomAppProto.DispenserStatus as DispenserStatus
import CustomAppProto.LightbulbStatus as LightbulbStatus
import CustomAppProto.Veggies as Veggies
import CustomAppProto.Drinks as Drinks
import CustomAppProto.DrinksCans as DrinksCans
import CustomAppProto.DrinksBottles as DrinksBottles
import CustomAppProto.Bread as Bread
from CustomAppProto.BreadType import BreadType
import CustomAppProto.Meat as Meat
from CustomAppProto.MeatType import MeatType
import CustomAppProto.DeviceStatus as DeviceStatus

# This is the method we will invoke from our driver program
# Note that if you have have multiple different message types, we could have
# separate such serialize/deserialize methods, or a single method can check what
# type of message it is and accordingly take actions.

'''
Find an input given output of enum

Example usage: key = type_to_key(MilkType)(0) where 0 is the value of the enum
'''
def get_key(func): 
    return lambda input: next(
        key for key, value in func.__dict__.items() if value == input
    )


def serialize(cm):
    builder = flatbuffers.Builder(0)

    # Depending on the message type, serialize differently
    if cm.type == "ORDER":
        # Serialize Milk list
        milk_offsets = []
        for milk_item in cm.order['milk']:
            Milk.MilkStart(builder)
            milk_type_value = getattr(MilkType, milk_item['type'], None)
            Milk.MilkAddType(builder, milk_type_value)
            Milk.MilkAddQuantity(builder, milk_item['quantity'])
            milk_offset = Milk.MilkEnd(builder)
            milk_offsets.append(milk_offset)
        
        # Create the Milk vector
        Order.OrderStartMilkVector(builder, len(milk_offsets))
        for offset in reversed(milk_offsets):
            builder.PrependUOffsetTRelative(offset)
        milk_vector = builder.EndVector(len(milk_offsets))

        # Start the Veggies object
        Veggies.VeggiesStart(builder)

        # Add each vegetable to the builder
        Veggies.VeggiesAddTomato(builder, cm.order['veggies']['tomato'])
        Veggies.VeggiesAddCucumber(builder, cm.order['veggies']['cucumber'])
        Veggies.VeggiesAddLettuce(builder, cm.order['veggies']['lettuce'])
        Veggies.VeggiesAddBroccoli(builder, cm.order['veggies']['broccoli'])
        Veggies.VeggiesAddSpinach(builder, cm.order['veggies']['spinach'])
        Veggies.VeggiesAddCarrots(builder, cm.order['veggies']['carrots'])

        # End the Veggies object and get the offset
        veggies = Veggies.VeggiesEnd(builder)

        # Serialize Drinks
        
        # Start the Drinks object
        drinks_cans = DrinksCans.DrinksCansStart(builder)

        # Add each can to the builder
        DrinksCans.DrinksCansAddCoke(builder, cm.order['drinks']['cans']['coke'])
        DrinksCans.DrinksCansAddBeer(builder, cm.order['drinks']['cans']['beer'])
        DrinksCans.DrinksCansAddLemonade(builder, cm.order['drinks']['cans']['lemonade'])

        # End the DrinksCans object and get the offset
        drinks_cans = DrinksCans.DrinksCansEnd(builder)

        # Start the DrinksBottles object
        drinks_bottles = DrinksBottles.DrinksBottlesStart(builder)

        # Add each bottle to the builder
        DrinksBottles.DrinksBottlesAddSprite(builder, cm.order['drinks']['bottles']['sprite'])
        DrinksBottles.DrinksBottlesAddGingerale(builder, cm.order['drinks']['bottles']['gingerale'])
        DrinksBottles.DrinksBottlesAddWater(builder, cm.order['drinks']['bottles']['water'])

        # End the DrinksBottles object and get the offset
        drinks_bottles = DrinksBottles.DrinksBottlesEnd(builder)

        # Start the Drinks object
        drinks = Drinks.DrinksStart(builder)

        # Add the DrinksCans and DrinksBottles offsets to the Drinks object
        Drinks.DrinksAddCans(builder, drinks_cans)
        Drinks.DrinksAddBottles(builder, drinks_bottles)

        # End the Drinks object and get the offset
        drinks = Drinks.DrinksEnd(builder)
        
        # Serialize Bread and Meat (similar to how Milk is serialized)
        bread_offsets = []
        for bread_item in cm.order['bread']:
            Bread.BreadStart(builder)
            bread_type_value = getattr(BreadType, bread_item['type'], None)
            Bread.BreadAddType(builder, bread_type_value)
            Bread.BreadAddQuantity(builder, bread_item['quantity'])
            bread_offset = Bread.BreadEnd(builder)
            bread_offsets.append(bread_offset)

        Order.OrderStartBreadVector(builder, len(bread_offsets))
        for offset in reversed(bread_offsets):
            builder.PrependUOffsetTRelative(offset)
        bread_vector = builder.EndVector(len(bread_offsets))

        meat_offsets = []
        for meat_item in cm.order['meat']:
            Meat.MeatStart(builder)
            meat_type_value = getattr(MeatType, meat_item['type'], None)
            Meat.MeatAddType(builder, meat_type_value)
            Meat.MeatAddQuantity(builder, meat_item['quantity'])
            meat_offset = Meat.MeatEnd(builder)
            meat_offsets.append(meat_offset)

        Order.OrderStartMeatVector(builder, len(meat_offsets))
        for offset in reversed(meat_offsets):
            builder.PrependUOffsetTRelative(offset)
        meat_vector = builder.EndVector(len(meat_offsets))

        # Start the Order FlatBuffer object
        Order.OrderStart(builder)

        # Add each of the fields
        Order.OrderAddVeggies(builder, veggies)
        Order.OrderAddDrinks(builder, drinks)

        # Assuming milk_vector, bread_offsets, and meat_offsets are offsets to already built vectors in the builder
        Order.OrderAddMilk(builder, milk_vector)
        Order.OrderAddBread(builder, bread_vector)
        Order.OrderAddMeat(builder, meat_vector)

        # End the Order FlatBuffer object
        serialized_msg = Order.OrderEnd(builder)

    elif cm.type == "HEALTH":
        # FIXME: Serialize Health correctly like above
        Health.HealthStart(builder)
        
        # Get attribute values
        dispenser_value = getattr(DispenserStatus, cm.health['dispenser'], None)
        Health.HealthAddDispenser(builder, dispenser_value)
        
        Health.AddIcemaker(builder, cm.health['icemaker'])
        
        lightbulb_value = getattr(LightbulbStatus, cm.health['lightbulb'], None)
        Health.HealthAddLightbulb(builder, lightbulb_value)
        
        Health.AddFridgeTemp(builder, cm.health['fridge_temp'])
        Health.AddFreezerTemp(builder, cm.health['freezer_temp'])
        
        sensor_value = getattr(DeviceStatus, cm.health['sensor_status'], None)
        Health.HealthAddSensorStatus(builder, sensor_value)

        filter_value = getattr(DeviceStatus, cm.health['water_filter'], None)
        Health.HealthAddWaterFilter(builder, filter_value)

        serialized_msg = Health.HealthEnd(builder)
        


    elif cm.type == "RESPONSE":
        # FIXME: Serialize Health correctly like above
        Response.ResponseStart(builder)
        Response.ResponseAddCode(builder, cm.response['code'])
        Response.ResponseAddContents(builder, cm.response['contents'])
        serialized_msg = Response.ResponseEnd(builder)

    # Finish the top-level message serialization
    # Start the Message object
    msg.MessageStart(builder)
    
    # Set the type of the message
    message_type = getattr(MessageType, cm.type, None)

    # Use msg.MessageAddType correctly
    msg.MessageAddType(builder, message_type)

    if cm.type == "ORDER":
        msg.AddOrder(builder, serialized_msg)
    elif cm.type == "HEALTH":
        msg.AddHealth(builder, serialized_msg)
    elif cm.type == "RESPONSE":
        msg.AddResponse(builder, serialized_msg)

    # close out the message
    final_msg = msg.End(builder)
    builder.Finish(final_msg)

    return builder.Output()


# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames (cm):
  """ serialize into an interable format """
  # We had to do it this way because the send_serialized method of zmq under the hood
  # relies on send_multipart, which needs a list or sequence of frames. The easiest way
  # to get an iterable out of the serialized buffer is to enclose it inside []
  print ("serialize custom message to iterable list")
  return [serialize (cm)]
  
  
# deserialize the incoming serialized structure into native data type
def deserialize(buf):

    # Placeholder for our custom message
    cm = CustomMessage()

    # Extract the main message from the buffer
    packet = msg.Message.GetRootAs(buf, 0)

    # Extract the message type
    cm.type = packet.Type()

    # Depending on the message type, deserialize differently
    if cm.type == MessageType.ORDER:
        order = packet.Order()
        if cm.order is None:
            cm.order = {}

        # Deserialize Milk
        cm.order['milk'] = []
        for i in range(order.MilkLength()):
            milk_item = order.Milk(i)
            cm.order['milk'].append({
                'type': get_key(MilkType)(milk_item.Type()),
                'quantity': milk_item.Quantity()
            })

        # Deserialize Veggies
        veggies = order.Veggies()
        cm.order['veggies'] = {
            'tomato': veggies.Tomato(),
            'cucumber': veggies.Cucumber(),
            'lettuce': veggies.Lettuce(),
            'broccoli': veggies.Broccoli(),
            'spinach': veggies.Spinach(),
            'carrots': veggies.Carrots()
        }

        # Deserialize Drinks
        drinks = order.Drinks()
        cans = drinks.Cans()
        bottles = drinks.Bottles()
        cm.order['drinks'] = {
            'cans': {
                'coke': cans.Coke(),
                'beer': cans.Beer(),
                'lemonade': cans.Lemonade()
            },
            'bottles': {
                'sprite': bottles.Sprite(),
                'gingerale': bottles.Gingerale(),
                'water': bottles.Water()
            }
        }

        # Deserialize Bread
        cm.order['bread'] = []
        for i in range(order.BreadLength()):
            bread_item = order.Bread(i)
            cm.order['bread'].append({
                'type': get_key(BreadType)(bread_item.Type()),
                'quantity': bread_item.Quantity()
            })

        # Deserialize Meat
        cm.order['meat'] = []
        for i in range(order.MeatLength()):
            meat_item = order.Meat(i)
            cm.order['meat'].append({
                'type': get_key(MeatType)(meat_item.Type()), 
                'quantity': meat_item.Quantity()
            })
        

    elif cm.type == MessageType.HEALTH:
        # FIXME: Deserialize Health correctly, similar to above
        health = packet.Health()
        if cm.health is None:
            cm.health = {}

        cm.health['dispenser'] = health.Dispenser()
        cm.health['icemaker'] = health.Icemaker()
        cm.health['lightbulb'] = health.Lightbulb()
        cm.health['fridge_temp'] = health.FridgeTemp()
        cm.health['freezer_temp'] = health.FreezerTemp()
        cm.health['sensor_status'] = health.SensorStatus()
        cm.health['water_filter'] = health.WaterFilter()
    

    elif cm.type == MessageType.RESPONSE:
        response = packet.Response()
        if cm.response is None:
            cm.response = {}

        cm.response['code'] = get_key(ResponseCode)(response.Code())
        cm.response['contents'] = response.Contents()

    # Convert the message type to a string
    

    cm.type = get_key(MessageType)(cm.type)

    return cm

# deserialize from frames
def deserialize_from_frames (recvd_seq):
  """ This is invoked on list of frames by zmq """

  # For this sample code, since we send only one frame, hopefully what
  # comes out is also a single frame. If not some additional complexity will
  # need to be added.
  assert (len (recvd_seq) == 1)
  #print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
  print ("received data over the wire = {}".format (recvd_seq[0]))
  cm = deserialize (recvd_seq[0])  # hand it to our deserialize method

  # assuming only one frame in the received sequence, we just send this deserialized
  # custom message
  return cm
    
