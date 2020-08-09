from eduponics_mqtt import mqtt
import json

# create array of soil moisture sensors
sensors = [{
    "id":0,
    "name":"Plant A",
    "enabled":1,
    "moisture":"100%"
},{
    "id":1,
    "name":"Plant B",
    "enabled":1,
    "moisture":"75%"
},{
    "id":2,
    "name":"Plant C",
    "enabled":1,
    "moisture":"25%"
},{
    "id":3,
    "name":"Plant D",
    "enabled":0,
    "moisture":"0%"
}]

# define environment array
environment_data = {
    "temp":25.0,
    "humidity":83.4,
    "sunlight":3000.0,
    "water_quantity":"Good"
}

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic.replace(MQTT.uuid + "/",""),str(msg.payload))
    if(msg.topic == "%s/plants/water" % MQTT.uuid):
        # get payload recieved in plants/water
        data = json.loads(msg.payload)
        # it can be "OK" payload from our script so we need to check the status is "pending"
        if(data["status"] == "pending"):
            # if it's pending, we need to take care of it by giving the plant water.
            give_water(client, userdata, msg, data)
    if(msg.topic == "%s/plants/soil" % MQTT.uuid):
        # get payload recieved in plants/water
        data = json.loads(msg.payload)
        # it can be "OK" payload from our script so we need to check the status is "pending"
        if(data["status"] == "pending" and data["action"] == "get"):
            # if it's pending, we need to take care of it by giving plant water.
            MQTT.update_multiple_soil_sensors(sensors)
    if(msg.topic == "%s/plants/environment" % MQTT.uuid):
        # get payload recieved in plants/water
        data = json.loads(msg.payload)
        # it can be "OK" payload from our script so we need to check the status is "pending"
        if(data["status"] == "pending" and data["action"] == "get"):
            # if it's pending, we need to take care of it by giving plant water.
            MQTT.update_environmental_data(environment_data)

def give_water(client, userdata, msg, data):
    # TODO: detect which plant need water and give it to him
    plant_key = data["key"]
    # publish response that water been given
    payload = {"key":plant_key,"status":"ok"}
    response = MQTT.publish_payload("plants/water",payload)
    print(response)
    client.close()

# initialize MQTT object from the eduponics_mqtt package
MQTT = mqtt.MQTT(
    address="mqtt.eclipse.org",
    port=1883,
    ts=60,
    on_message_callback=on_message
)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
MQTT.client.loop_forever()
