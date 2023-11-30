    #4. 실시간으로 정보를 전송한다.
    #4-1. 웹페이지가 켜지면 visiter.txt 파일을 읽는다.
# MQTT
import datetime
import time
import paho.mqtt.client as mqtt
import PublicBathroom

ip = "localhost"

def on_connect(client, userdata, flag, rc):
    client.subscribe("check_cleaning", qos = 0)

def on_message(client, userdata, msg):
    PublicBathroom.cleaning_day = msg.payload;
    print(msg.payload)
    print(PublicBathroom.cleaning_day)

# 메인 함수
client = mqtt.Client()
client.connect(ip, 1883)
client.loop_start()

client.on_connect = on_connect
client.on_message = on_message

# 모든 데이터는 Day_Of_User_Data를 통해 관리된다.
day_of_user_data = {}

PublicBathroom.get_day_of_user_data(day_of_user_data)
now  = datetime.datetime.now()
nowString = now.strftime("%Y-%m-%d")

PublicBathroom.count_person = day_of_user_data[nowString].get_day_of_user()
PublicBathroom.count_bath = day_of_user_data[nowString].get_day_of_bath()
PublicBathroom.cleaning_day = day_of_user_data[nowString].get_cleaning_day()

while True:
    distance_outside = PublicBathroom.measure_distance(PublicBathroom.trig_outside, PublicBathroom.echo_outside) #성공
    distance_inside = PublicBathroom.measure_distance(PublicBathroom.trig_inside, PublicBathroom.echo_inside) #성공
    if distance_outside<50: 
        check_outside_sensor = True 
    else:
        check_outside_sensor = False
        
    if distance_inside<50:
        check_inside_sensor = True
    else:
        check_inside_sensor = False

    PublicBathroom.check_to_go_inside(check_inside_sensor, check_outside_sensor) # 성공
    PublicBathroom.check_to_go_outside(check_inside_sensor, check_outside_sensor) # 성공
    PublicBathroom.check_bath(PublicBathroom.sensor, PublicBathroom.ledGreen) # 성공
    time.sleep(0.5)

    #데이터를 PublicBathroom 전역변수에 모두 저장 중
    PublicBathroom.set_day_of_user_data(day_of_user_data, PublicBathroom.count_person, PublicBathroom.count_bath, PublicBathroom.cleaning_day)

    client.publish("dataCountPerson", day_of_user_data[nowString].get_day_of_user(), qos=0)
    client.publish("dataCountBath", day_of_user_data[nowString].get_day_of_bath(), qos=0)
    client.publish("dataNowPerson", PublicBathroom.now_person, qos=0)
    client.publish("dataBathNow", PublicBathroom.bath_now, qos=0)
    client.publish("dataCleaning", PublicBathroom.cleaning_day, qos=0)
    
client.loop_stop()
client.disconnect()