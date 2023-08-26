#### SERIAL CONNECTION ####
connectionType = "serial"
port = "/dev/ttyUSB0"

#### TCP CONNECTION ####
#connectionType = "cp"
#ipAddress= "127.0.0.1"
#port = "2000"

#Inverter address. (Usually 2 unless multple inverters are connected.)
inverterAddress = 2

#### MQTT CONNECTION DETAILS ####
mqttServer = "ENTER HOME ASSISTANT IP ADDRESS...."
mqttPort = 1883
mqttUsername = "MOSQUITO USERNAME...."
mqttPassword = "MOSQUITO PASSWORD....";

#### POLL INTERVAL TIME (seconds) ####
sleepTime = 10;

#### OPTIONS ####
# Send MQTT server '0 W' and '0 V' message when inverter connection fails.
sendMQTTOnConnectionError = True;