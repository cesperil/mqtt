import paho.mqtt.client as mqtt
import requests
import RPi.GPIO as GPIO

servidor = "192.168.1.14"
puerto = "8084"
broker = "192.168.1.10"

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

def encenderApagarLuces(valor):

        if valor=="b'1'":
                return encenderLuces();
        else:
                return apagarLuces();

def encenderLuces():
        GPIO.output(17,True);
        return "Activado"

def apagarLuces():
        GPIO.output(17, False);
        return "Desactivado"



def on_message(mqttc, obj, msg):
	if msg.topic == "activador":
		print(str(msg.payload));
		print(encenderApagarLuces(str(msg.payload)));
	else:
		print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
		print('http://'+servidor+":"+puerto+"/Agrotente&"+msg.topic+"=1:"+str(msg.payload))
		req = requests.get('http://'+servidor+":"+puerto+"/Agrotente/?"+msg.topic+"="+str(msg.payload))



#iniciamos cliente mqtt
mqttc = mqtt.Client()
mqttc.on_message = on_message

#conectar con el broker para suscripciones
mqttc.connect(broker, 1883, 60)
mqttc.subscribe("temperatura", 0)
mqttc.subscribe("humedad",0)
mqttc.subscribe("activador",0)
mqttc.loop_forever()


