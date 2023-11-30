import time
import datetime
import RPi.GPIO as GPIO
# 온습도 센서
from adafruit_htu21d import HTU21D
import busio
# 조도 센서
import Adafruit_MCP3008

# 조도 센서
mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

# GPIO 속성 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# led 조명 핀번호 입력
ledWhite = 17
ledGreen = 27
GPIO.setup(ledWhite, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)

# 스위치 센서 핀번호 입력
button = 21
btn_status = 0
GPIO.setup(button, GPIO.IN, GPIO.PUD_DOWN)

# 초음파 센서 핀번호 입력
    # 말단 부분
echo_outside = 23
trig_outside = 24
GPIO.setup(trig_outside, GPIO.OUT)
GPIO.setup(echo_outside, GPIO.IN)

    # 머리부분
echo_inside = 5
trig_inside = 6
GPIO.setup(trig_inside, GPIO.OUT)
GPIO.setup(echo_inside, GPIO.IN)

# 온습도 센서 핀번호 입력
sda = 2
scl = 3 
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c)

# led 조명
def led_on_off(pin, value):
    GPIO.output(pin, value)

# 스위치 센서
def button_pressed(pin):
    global btn_status
    global led
    btn_status = 0 if btn_status == 1 else 1
    led_on_off(led, btn_status)

# 초음파 센서
def measure_distance(trig, echo):
    # 한번 초음파 발사
    GPIO.output(trig, 1)
    GPIO.output(trig, 0)

    # 들어오는 echo 정보 초기화
    while(GPIO.input(echo)==0):
        pass

    # 지금부터 시간 측정시작
    pulse_start = time.time()

    # echo가 0에서 1로 다시 변할 때까지 루프
    while(GPIO.input(echo)==1):
        pass
    
    # 끝난 시간 입력
    pulse_end = time.time()
    
    #시간 차를 통한 거리(실수) 측정 및 전송
    pulse_duration = pulse_end - pulse_start
    return pulse_duration*340*100/2


# 온습도 센서
def getTemperature(sensor):
    return float(sensor.temperature)

def getHumidity(sensor):
    return float(sensor.relative_humidity)

#프로그램 코드
# 사람이 포착되는 경우는 네가지 이다. 1) 밖에서만 포착, 2) 안에서만 포착, 3) 밖에 포착된 채로 안에서 포착, 4) 안에서 포착된 채로 밖에서 포착

#1. 사람이 들어오는 것을 탐지한다.

# 1), 3) 경우 체크
### 예외처리 필요: 사람이 안에 있는 중에 해가 진 경우 ###
def check_to_go_inside(check_inside_sensor, check_outside_sensor):
        global now_person
        global count_person
        global ready_check_to_go_inside
        global ledWhite
        
        # focus가 true인데 센서 두개에서 모두 측정된 상황 (사람이 통과하기 직전)
        if(ready_check_to_go_inside == True and check_outside_sensor == True and check_inside_sensor == True):
            # (2-1)
            if now_person==0:
                turn_on_light(ledWhite, True)
            count_person = count_person + 1 # 하루 이용자 수 증가
            now_person = now_person + 1 # 사람이 안에 있다.
            print("당일 인원: "+str(count_person))
            print("내부 인원: "+str(now_person))
            print()
        else:
            ready_check_to_go_inside = False

        # 밖에서 안으로 들어오는 중
        if(check_outside_sensor==True and check_inside_sensor==False):
            ready_check_to_go_inside = True
        else:
            ready_check_to_go_inside = False # 예외처리: 기존에 들어가다가(true) 다시 나온 상황

# 2), 4) 경우 체크
def check_to_go_outside(check_inside_sensor, check_outside_sensor):
        global ready_check_to_go_outside
        global now_person
        global ledWhite
        # focus가 true인데 센서 두개에서 모두 측정된 상황 (사람이 통과하기 직전)
        if(ready_check_to_go_outside == True and check_outside_sensor == True and check_inside_sensor == True):
            # (2-1)
            if now_person > 0:
                now_person = now_person - 1
            if now_person == 0:
                turn_on_light(ledWhite, False)
            print("당일 인원: "+str(count_person))
            print("내부 인원: "+str(now_person))
            print()
        else:
            ready_check_to_go_outside = False

        # 밖에서 안으로 들어오는 중
        if(check_outside_sensor==False and check_inside_sensor==True):
            ready_check_to_go_outside = True
        else:
            ready_check_to_go_outside = False # 예외처리: 기존에 들어가다가(true) 다시 나온 상황

#2. 조도의 양을 판단한다.
### 기준 값 수정해야함 ###
### 2-2. 스피커를 킨다. <-- 추가해야함 ###

    #2-1. 조명을 킨다.
def turn_on_light(ledWhite, on_off):
    global SUNLIGHTHOLD

    sunlight = mcp.read_adc(0)
    print("sunlight: "+str(sunlight)) #test
    print()
    
    # 조명이 켜져있지 않고, 사람이 있을 경우에만 실행
    if SUNLIGHTHOLD < sunlight and on_off == True:
        print("켜짐") #test
        print()
        led_on_off(ledWhite, 1)
    elif SUNLIGHTHOLD > sunlight or not(on_off) == True:
        print("꺼짐") #test
        print()
        led_on_off(ledWhite, 0)


#3. 온습도 센서를 독자적으로 관리한다.

def check_bath(sensor, ledGreen):
        global count_bath
        global previous_temperature
        global flag_on_off
        global bath_now

        current_temperature = getTemperature(sensor)

        #3-1. 환풍기를 킨다.
            # 한번만 켜지면 되기에 이전에 이미 켰다면 환풍기 실행안함
        if previous_temperature + 0.1 < current_temperature and flag_on_off == False and previous_temperature != 0:
            count_bath = count_bath + 1 # 변기 사용자 수 증가
            bath_now = 1
            print("변기 인원: "+str(count_bath))
            print()
            flag_on_off = True
            led_on_off(ledGreen,1)
        elif previous_temperature - 0.1 > current_temperature and flag_on_off == True:
            bath_now = 0
            print("변기 인원: 나감")
            print()
            flag_on_off = False
            led_on_off(ledGreen,0)
        else:
            pass
        previous_temperature = current_temperature

# 날짜 별 데이터 저장을 위함
class Day_Of_User_Data:
    #key 값은 당일 날짜이다.
    def __init__(self, day_of_user, day_of_bath, cleaning_day):
        self.day_of_user = day_of_user
        self.day_of_bath = day_of_bath
        self.cleaning_day = cleaning_day
    
    #getter 함수
    def get_day_of_user(self):
        return self.day_of_user
    
    def get_day_of_bath(self):
        return self.day_of_bath
    
    def get_cleaning_day(self):
        return self.cleaning_day

# 데이터 저장함수
def get_day_of_user_data(day_of_user_data):
    line = []
    file = open("./data/data.txt","r")
    flag = False
    #저장 형식: 2023-11-22/13,2
    for aline in file.readlines():
        aline = aline.strip()
        print(aline)
        if flag == False:
            line.append(aline[0:aline.find('/')])
            line.append(aline[aline.find('/')+1:aline.find('|')])
            line.append(aline[aline.find('|')+1:aline.find('`')])
            line.append(aline[aline.find('`')+1:len(aline)])
            flag = True
        else:
            line[0] = aline[0:aline.find('/')]
            line[1] = aline[aline.find('/')+1:aline.find('|')]
            line[2] = aline[aline.find('|')+1:aline.find('`')]
            line[3] = aline[aline.find('`')+1:len(aline)]

        day_of_user_data[line[0]] = Day_Of_User_Data(int(line[1]), int(line[2]), line[3])
    file.close()

# 데이터 기록함수
def set_day_of_user_data(day_of_user_data, count_person, count_bath, cleaning_day):
    now  = datetime.datetime.now()
    nowString = now.strftime("%Y-%m-%d")
    if day_of_user_data[nowString].get_day_of_user() == count_person and day_of_user_data[nowString].get_day_of_bath() == count_bath :
        return
    else:
        day_of_user_data[nowString] = Day_Of_User_Data(count_person, count_bath, cleaning_day)

    file = open('./data/data.txt','w')
    #저장 형식: 2023-11-22/13|2`2023-11-21

    for key in day_of_user_data.keys():
        file.write("%s/%s|%s`%s\n"% (key, day_of_user_data[key].get_day_of_user(), day_of_user_data[key].get_day_of_bath(), day_of_user_data[key].get_cleaning_day()))
    file.close()


# 전역 변수
count_person = 0
count_bath = 0
cleaning_day = "none"

now_person = 0
bath_now = 0

check_inside_sensor = False
check_outside_sensor = False

ready_check_to_go_inside = False
ready_check_to_go_outside = False

SUNLIGHTHOLD = 0

previous_temperature = 0.0
flag_on_off = False
getTemperature(sensor)

led_on_off(ledWhite,0)
led_on_off(ledGreen,0)