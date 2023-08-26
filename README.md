
# AurorapyToMqtt 

Library to send data from serial or TCP communication from Aurora Inverters (ABB) to MQTT.
Tested on Raspberry Pi using USB serial adapter.

**Fork with improved error handling and easier configuration of serial connections.**

# Home Assistant
Even though home assistant has its own library to communicate with the inverter, in my opinion it is not very well implemented. You can only use serial communication and the only data returned are actual power, total energy produced and temperature. I was not even able to implement the data in the new energy dashboard. I tried to look at the library but I really don't know where to start to implement these changes. So for now I provide the template to read the data from mqtt.

# Home Assistant Installation
1. Ensure you have a MQTT broker setup for home assistant. (If starting fresh follow the 'Run your own Server' section of this guide: https://www.home-assistant.io/integrations/mqtt/)
2. Download this repository to your computer.
3. Enter the correct parameters in the **Config.py** file.

	* The supplied config is setup for a serial connection to the inverter. 
	However to use TCP, uncomment that section of the file and comment out the serial connection section.
	
	* Next enter your MQTT server details, if you have followed the mosquito guide. This should be as simple as entering the IP address of your home assistant installation, and the username and password from this section of your MQTT integration settings: 
	![enter image description here](https://i.ibb.co/64SvtHZ/MQTT.jpg)
	
5. Finally, run the python script, and verify that the script is able to communicate with both the inverter and your mqtt server. 

**If all is well you should see the following message:**

```
6. Successfully fetched statistics from Aurora PowerOne Inverter.
7. Successfully connected to MQTT server.
8. Inverter statistics successfully delivered to server.

Waiting for next cycle...
```
# Accessing Readings on Dashboard
Place this code at the end of your **configuration.yaml** home assistant file and reboot. The solar sensors should now be listed as entities under home assistant. 

```
mqtt:

sensor:

- name: "Solar Panel Power"

state_topic: "/solar/1"

unit_of_measurement: "W"

value_template: "{{ value_json.output_power | round(1)}}"

device_class: "power"

state_class: "measurement"

- name: "Solar Panel Voltage"

state_topic: "/solar/1"

unit_of_measurement: "V"

value_template: "{{ value_json.input_voltage | round(1)}}"

device_class: "voltage"

state_class: "measurement"

- name: "Solar Panel Current"

state_topic: "/solar/1"

unit_of_measurement: "A"

value_template: "{{ value_json.input2_current | round(1)}}"

device_class: "current"

state_class: "measurement"

- name: "Solar Panel Daily Production"

state_topic: "/solar/1"

unit_of_measurement: "kWh"

value_template: "{{ value_json.daily_energy | round(1)}}"

device_class: "energy"

state_class: "total"

- name: "Solar Panel Weekly Production"

state_topic: "/solar/1"

unit_of_measurement: "kWh"

value_template: "{{ value_json.energy_week | round(1)}}"

device_class: "energy"

state_class: "total"

- name: "Solar Panel Montly Production"

state_topic: "/solar/1"

unit_of_measurement: "kWh"

value_template: "{{ value_json.energy_month | round(1)}}"

device_class: "energy"

state_class: "total"

- name: "Solar Panel Annual Production"

state_topic: "/solar/1"

unit_of_measurement: "kWh"

value_template: "{{ value_json.year_energy | round(1)}}"

device_class: "energy"

state_class: "total"

- name: "Solar Panel Total Production"

state_topic: "/solar/1"

unit_of_measurement: "kWh"

value_template: "{{ value_json.energy_total | round(1)}}"

device_class: "energy"

state_class: "total_increasing"

- name: "Solar Panel Temperature"

state_topic: "/solar/1"

unit_of_measurement: "°C"

value_template: "{{ value_json.inverter_temperature | round(1)}}"
```