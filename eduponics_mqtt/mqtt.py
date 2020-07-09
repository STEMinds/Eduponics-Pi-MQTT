#!/usr/bin/python

#Copyright (c) 2020 Roni Gorodetsky for STEMinds
#Website: https://steminds.com

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.


import paho.mqtt.client as paho_mqtt
import json
import uuid
import os
import pyqrcode

'''
topics:
app/auth - auth with mobile app and user custom ID
plants/soil - report soil moisture level i.e: {'id':'A','name':'plant A','enabled':true,'moisture':'50%'}
plants/environment - report the environment i.e: {'temp':25,'humidity':'60%','light':'3000','has_water':true,'flow_speed':0}
plants/water - command service for giving water to plants i.e: {'plant_id':'A'}
'''

class MQTT:

    def __init__(self,address="mqtt.eclipse.org",port=1883,ts=60,uuid=None,on_connect_callback=None,on_message_callback=None):
        # set debugging true or false
        self.debug = True
        # check if user supplied unique id
        # if not, get it as raspberry pi serial number
        self.uuid = uuid
        if(self.uuid == None):
            self.get_uuid()
        # TODO: make sure if uuid supplid that it's type UUID and not random string
        # give properties to the object
        self.address = address
        self.port = port
        self.ts = ts
        # create the client
        self.client = paho_mqtt.Client()
        # connect to the client
        self.client.connect(self.address, self.port, self.ts)
        # redirect call backs to on_connect and on_message
        if(on_connect_callback != None):
            self.client.on_connect = on_connect_callback
        else:
            self.client.on_connect = self.on_connect
        if(on_message_callback != None):
            self.client.on_message = on_message_callback
        else:
            self.client.on_message = self.on_message

    def get_uuid(self):
        if(os.path.exists('./uuid.txt') == False):
            # generate unique ID
            self.uuid = str(uuid.uuid1())
            # save the unique id into text file
            with open("uuid.txt", "w") as text_file:
                text_file.write(self.uuid)
            # generate QR code of the uuid
            qrCode = pyqrcode.create(self.uuid)
            print(qrCode.terminal(quiet_zone=1))
        else:
            # file already exist, get uuid from it
            file = open('uuid.txt', 'r')
            self.uuid = file.readlines()
            if(self.uuid == []):
                # uuid file found but it's empty,
                # generate new one and put it inside
                self.uuid = str(uuid.uuid1())
                with open("uuid.txt", "w") as text_file:
                    text_file.write(self.uuid)
            else:
                # TODO: make sure the uuid from the file is valid uuid
                self.uuid = self.uuid[0]
            # generate QR code of the uuid
            qrCode = pyqrcode.create(self.uuid)
            print(qrCode.terminal(quiet_zone=1))
            print("======================================================")
            print("Welcome to STEMinds Eduponics mobile app MQTT service")
            print("======================================================")
            print("")
            print("Your uuid code is %s" % self.uuid)
            print("")
            print("This unique ID is your personal MQTT identifier, DO NOT SHARE IT WITH ANYONE ELSE!")
            print("The Unique ID is stored inside uuid.txt file located in your root directory.")
            print("If you remove the file or the uuid inside, new one will be generated.")
            print("Go to settings in STEMinds Eduponics mobile app and manually enter the code or scan the QR code above,")
            print("Then press connect. By connecting you'll be able to share sensors information from your Raspberry Pi to the mobile app.")
            print("")
            print("To avoid this message next time, supply uuid argument to MQTT class when initializing.")
            print("")

    def update_single_soil_sensor(self,sensor_data):
        response = self.publish_payload("plants/soil",sensor_data)
        return response

    def update_multiple_soil_sensors(self,sensors_data):
        response = self.publish_payload("plants/soil",sensors_data)
        return response

    def update_environmental_data(self,environmental_data):
        response = self.publish_payload("plants/environment",environmental_data)
        return response

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if(str(rc) == "0"):
            print("[-] Connected to MQTT server successfully")
        else:
            print("[!] Something went wrong, result code %s" % rc)
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # here subscribe to topics
        topics = ["plants/soil","plants/environment","plants/water"]
        for topic in topics:
            client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        # there are no functions in this callback
        # if you want to add functions, define your own callback on your main .py file
        print(msg.topic+" "+str(msg.payload))

    def publish_payload(self,topic,payload):
        # create a list of allowed topics
        allowed_topics = ["plants/soil","plants/environment","plants/water"]
        # check if the topic is allowed
        if(topic not in allowed_topics):
            return {"message":"the topic is not in the allowed topics list","error":True,"allowed_topics":allowed_topics}
        # we need to make sure the payload is list or dictionary (depends on the topic)
        if(type(payload) == type({}) or type(payload) == type([{}])):
            if(topic == "plants/environment"):
                # define allowed keys
                allowed_keys = ["temp","humidity","sunlight","water_quantity"]
                # we will need to do some verification on the data to make sure it's clean
                # go through each item on the payload
                for key in payload:
                    # check the key names if they are in the allowed list
                    if(key not in allowed_keys):
                        # there is a key that is not allowed by the API dataset
                        return {"message":"one or more of your keys are not allowed","error":True,"allowed_keys":allowed_keys}
                # check if temp is type integer
                if(type(payload["temp"]) != type(0.1)):
                    # temp must be float
                    return {"message":"temp value must be a float","error":True}
                # check if humidity is type float
                if(type(payload["humidity"]) != type(0.1)):
                    # humidity must be float
                    return {"message":"humidity value must be a float","error":True}
                # check if sunlight is type int
                if(type(payload["sunlight"]) != type(0.1)):
                    # sunlight must be float
                    return {"message":"sunlight value must be a float","error":True}
                # check if water quantity is type string
                if(type(payload["water_quantity"]) != type("")):
                    # water quantity must be string
                    return {"message":"water quantity value must be a string","error":True}

                # if we reached here, let's publish environmental data
                # to plants/environment topic
                self.client.publish("plants/environment",str(payload).replace("'",'"'))
                return {"message":"OK","error":False}
            # first we need to make sure the payload is dictionary
            if(topic == "plants/soil"):
                # define allowed keys
                allowed_keys = ["id","name","enabled","moisture"]
                # we will need to do some verification on the data to make sure it's clean
                # go through each item on the payload
                for item in payload:
                    # check the key names if they are in the allowed list
                    for key in item:
                        if(key not in allowed_keys):
                            # there is a key that is not allowed by the API dataset
                            return {"message":"one or more of your keys are not allowed","error":True,"allowed_keys":allowed_keys}
                    # check if ID is type integer
                    if(type(item["id"]) != type(0)):
                        # ID must be integer
                        return {"message":"id value must be an integer","error":True}
                    # check if name is type string
                    if(type(item["name"]) != type("")):
                        # name must be string
                        return {"message":"name value must be string","error":True}
                    # check if enabled is type int
                    if(type(item["enabled"]) != type(0)):
                        # enabled must be string
                        return {"message":"enabled value must be type int, either 0 or 1","error":True}
                    # also check the enabled is either 0 or 1
                    elif(item["enabled"] < 0 or item["enabled"] > 1):
                        # enabled must be either 1 or 0
                        return {"message":"enabled value must be either 1 or 0","error":True}
                    # check if moisture is string and include precent
                    if(type(item["moisture"]) != type("")):
                        # moisture must be string
                        return {"message":"moisture must be string and include % at the end","error":True}
                    # also check that there is "%" at the end
                    elif(item["moisture"][-1:] != "%"):
                        # moisture last character must be %
                        return {"message":"moisture last character must be precentage","error":True}
                # if we reached here, let's publish
                # for each item in the payload, publish it to plants/soil topic
                for item in payload:
                    self.client.publish("plants/soil",str(item).replace("'",'"'))
                return {"message":"OK","error":False}
        else:
            return {"message":"payload is not a dictionary or list","error":True}
