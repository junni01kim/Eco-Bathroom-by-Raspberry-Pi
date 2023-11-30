# Eco-Bathroom-by-Raspberry-Pi

#### 다음 프로그램의 작동은 이렇습니다.
1. mqtt가 작동해야한다.
  - mqtt는 mosquitto를 사용합니다.
  - __*PublicBathroomMqtt.py*__ 소스 코드에 각자의 mosquitto를 실행하고 있는 LAN의 주소를 작성합니다.
2. 웹페이지를 통해 작동한다.
  - 웹페이지는 html과 javascript로 되어있으며, 토픽 신청기능과 그래프 출력 버튼이 있습니다.
  - __*View.html*__을 통해 당일의 날짜, 당일 이용자 수, 당일 변기 이용자 수, 최근 청소일자를 확인할 수 있습니다.

#### 다음 프로그램은 이러한 유의 사항이 있습니다.
1. 초음파 센서 인식이 명확하지 않습니다. 본인이 사용한 초음파 센서는 저가 장치를 사용하였습니다.
   -  주변 3m 전방에 벽이 없거나, 반사가 잘 되지 않으면 작동이 오류가 납니다.
2. 조도 센서가 이상이 발생합니다. 본인이 사용한 조도센서는 상대적인 조도 값을 이용했습니다.
   - 이용하려는 조도 센서에 따라 약간의 코드 수정이 필요할 수 있습니다.
