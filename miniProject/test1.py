import paho.mqtt.client as mqtt

def on_connect(client, userdata, flag, rc):
    client.subscribe("letter", qos = 0)
    client.subscribe("dataCountPerson", qos = 0)
    client.subscribe("dataCountBath", qos = 0)
    client.subscribe("dataNowPerson", qos = 0)
    client.subscribe("dataBathNow", qos = 0)

def on_message(client, userdata, msg):
    print(msg.topic, end=", ")
    print(str(msg.payload.decode("utf-8")))

    if msg.topic == "dataCountPerson" :
        countPerson = str(msg.payload.decode("utf-8"))
        print(countPerson)

    if msg.topic == "dataCountBath" :
        countBath = str(msg.payload.decode("utf-8"))
        print(countBath)

    if msg.topic == "dataNowPerson" :
        now_user = str(msg.payload.decode("utf-8"))
        print(now_user)

    if(msg.topic == "dataBathNow") :
        bathNow = str(msg.payload.decode("utf-8"))
        print(bathNow)

ip = "192.168.180.135"
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ip, 1883)
client.loop_forever()