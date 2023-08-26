from aurorapy.client import AuroraError, AuroraSerialClient
from aurorapy.client import AuroraError, AuroraTCPClient
import time
import paho.mqtt.client as mqtt
import json
import Config


# The callback for when the client receives a CONNACK response from the server.
def on_connect(mqtt, userdata, flags, rc):
  
    if rc==0:
        pass
        
    else:
        print("Error: Unable to Establish connection to MQTT server.\n\nError Message: ")
        print(rc)


# The callback for when a PUBLISH message is received from the server.
def on_message(mqtt, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def ConnectMQTT(mqtt):
    try:
       mqtt.connect(Config.mqttServer, Config.mqttPort, 60)
       print("2. Successfully connected to MQTT server.")
       mqtt.loop_start()
       
       return True
    except Exception as err:
        print("2. Error: Unable to setup connection to MQTT server.\n\nError Message: ")
        print(err)
        return False

def ConnectAurora(aurora):
    try:
        aurora.connect()
        
    except AuroraError as err:
        
        if(str(err) != "Port is already open."):
            print("1. Error: Unable to Establish connection to inverter.\n\nError Message: ")
            print(err)
            print(type(err.args[0]))
            return False;

    #print("1. Successfully connected to Aurora PowerOne Inverter.")
    return True;


def ProcessPoll(aurora, mqtt):
    result = dict()
    try:
        # OUTPUT POWER
        output_power = aurora.measure(3)
        result["output_power"] = output_power
        print("Power:", output_power, "W")

        # INPUT 1 VOLTAGE
        input_voltage = aurora.measure(23)
        print("Voltage:", input_voltage, "V")
        result["input_voltage"] = input_voltage

        ampsTot = 0
        # INPUT 1 CURRENT
        input1_current = aurora.measure(25)
        print("Amps1:", input1_current, "A")
        ampsTot += input1_current

        # INPUT 2 CURRENT
        input2_current = aurora.measure(27)
        print("Amps2:", input2_current, "A")
        ampsTot += input2_current
        result["input2_current"] = input2_current

        # ENERGY DAILY
        daily_energy = aurora.cumulated_energy(period=0) / 1000
        print("Energy Daily:", daily_energy, "kWh")
        result["daily_energy"] = daily_energy

        # ENERGY WEEK
        energy_week = aurora.cumulated_energy(period=1) / 1000
        print("Energy Week:", energy_week, "kWh")
        result["energy_week"] = energy_week

        # ENERGY MONTH
        energy_month = aurora.cumulated_energy(period=3) / 1000
        print("Energy Month:", energy_month, "kWh")
        result["energy_month"] = energy_month

        # ENERGY YEAR
        year_energy = aurora.cumulated_energy(period=4) / 1000
        print("Energy Year:", year_energy, "kWh")
        result["year_energy"] = year_energy

        # ENERGY TOTAL
        energy_total = aurora.cumulated_energy(period=5) / 1000
        print("Energy Total:", energy_total, "kWh")
        result["energy_total"] = energy_total

        inverter_temperature = aurora.measure(21)
        print("Inverter Temperature:", inverter_temperature, "Â°C")
        result["inverter_temperature"] = inverter_temperature
        
        print("1. Successfully fetched statistics from Aurora PowerOne Inverter.")

    except AuroraError as err:
       print("1. Error: Unable to fetch statistics from Aurora PowerOne Inverter. \n\nError Message: ")
       print(err)
      
       if(Config.sendMQTTOnConnectionError == False): return

       # OUTPUT POWER
       result["output_power"] = 0
       result["input_voltage"] = 0
       result["input1_current"] = 0
       result["input2_current"] = 0
   

    if(ConnectMQTT(mqtt)):

        try:   
            jsonRes = json.dumps(result)
            publish = mqtt.publish("/solar/1", jsonRes)
            
            #publish.wait_for_publish()
       
            print("3. Inverter statistics successfully delivered to server.")
        
        except Exception as err:
            print("3. Error: An error occurred while processing the inverter statistics.\n\nError Message: ")
            print(err)


def PerformPoll(aurora, mqtt):
    if(ConnectAurora(aurora)): ProcessPoll(aurora, mqtt)        

    print("\nWaiting for next cycle...")
    
    print("-----------------------------------------------------------------------")
    

mqtt = mqtt.Client()
mqtt.on_connect = on_connect
mqtt.on_message = on_message
mqtt.username_pw_set(
    Config.mqttUsername, Config.mqttPassword)

aurora = 0

if(Config.connectionType == "serial"):
    aurora = AuroraSerialClient(port=Config.port, address=Config.inverterAddress)
elif(Config.connectionType == "tcp"):
    aurora = AuroraTCPClient(ip=Config.ipAddress, port=Config.port, address=Config.inverterAddress)


print("Script started. Connecting to inverter. Please wait...")

while True:
   PerformPoll(aurora, mqtt)
   time.sleep(Config.sleepTime)