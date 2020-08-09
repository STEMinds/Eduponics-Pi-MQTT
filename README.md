# Eduponics-Pi-MQTT

Python3 MQTT package for the Eduponics react-native mobile app

## Usage instructions

### Package functions

The package includes multiple functions

first, you'll need to intialize the connection to the MQTT server.

for now, it's not possible to change the server and we use **mqtt.eclipse.org**, this will be changed in the near future.

then, you need to generate a unique UUID in order to connect the hardware to the app, you can do this by calling the **.get_uuid()** function

then we have the function **.update_multiple_soil_sensors()** to update a dict of sensors all together.

or, we can update only one sensor with **.update_single_soil_sensor()**

In case we want to update environmental sensors such as: light, temperature, humidity, water quantity etc .. we can do this with **.update_environmental_data**

## About us

We are STEMinds, a tiny startup based in Shenzhen, China.
Our mission is to design cutting edge hardware kits to teach the skills of the future.
We work hard to develop subject based kits to teach hands STEM subjects with ease.

## Support us

We work very hard to develop our custom hardware kits and still not a single one is available for purchase.
kits takes time, effort and money to develop. During such unprecedented times, it's difficult to get funded.
That doesn't stop us from giving back to the community and doing our best effort to get involved and create impact, even without earning a penny.
Support us by spreading the word and if you feel generous, you can buy us a coffee!
![Buy us coffee at ko-fi.com/steminds](https://storage.ko-fi.com/cdn/useruploads/7bc362f8-727b-49dd-8cf7-50e347b5a2bf.png)
feel free to treat us at [ko-fi.com/STEMinds](ko-fi.com/STEMinds) - for you it's 5$ for us it's to keep doing what we love the most.

## Special thanks

We would like to thank some special contributors to the entire STEMinds Eduponics mobile app project

### Translations

For our mobile app language translators

STEMinds - Hebrew, English, Chinese
Akshay Vernekar - Hindi
Amanda Elnecave - Português
David Motsch - German
Lưu Đức Toàn - Vietnamese

## Play store featured design

For our features play store picture we would like to thank Hotpot Design
Feel free to visit them at hotpot.ai to get your own amazing designs at no time.

## Bug reporting

Feel free to report a bug through the app to our email at contact@steminds.com
It will be even better if you can repot us through github and we will follow us to fix it.
any contribution is welcome. we are looking to improve but not often have the time and resources to do it all.

## TODO List
