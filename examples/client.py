from eduponics_mqtt import mqtt
import json

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if(msg.topic == "plants/water"):
        # get payload recieved in plants/water
        data = json.loads(msg.payload)
        # it can be "OK" payload from our script so we need to check the status is "pending"
        if(data["status"] == "pending"):
            # if it's pending, we need to take care of it by giving plant water.
            give_water(client, userdata, msg, data)

def give_water(client, userdata, msg, data):
    # TODO: detect which plant need water and give it to him
    plant_key = data["key"]
    # publish response that water been given
    client.publish("plants/water",str({"key":plant_key,"status":"OK"}).replace("'",'"'))
    client.close()

# initialize MQTT object from the eduponics_mqtt package
MQTT = mqtt.MQTT(
    address="mqtt.eclipse.org",
    port=1883,
    ts=60,
    on_message_callback=on_message
)

def main():
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
        "moisture":"25%"
    }]

    # define environment array
    environment_data = {
        "temp":25.0,
        "humidity":83.4,
        "sunlight":3000.0,
        "water_quantity":"Good"
    }

    response = MQTT.update_multiple_soil_sensors(sensors)
    print(response)
    response = MQTT.update_environmental_data(environment_data)
    print(response)

# run the main application
main()
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
MQTT.client.loop_forever()
