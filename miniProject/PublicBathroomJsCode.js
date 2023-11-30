let client = null; // MQTT 클라이언트의 역할을 하는 Client 객체를 가리키는 전역변수
let connectionFlag = false; // 연결 상태이면 true
const CLIENT_ID = "client-"+Math.floor((1+Math.random())*0x10000000000).toString(16) // 사용자 ID 랜덤 생성

let Topic;
let Message;

let check_Cleaning;

function connect() { // 브로커에 접속하는 함수  
	if(connectionFlag == true)
		return; // 현재 연결 상태이므로 다시 연결하지 않음
	// 사용자가 입력한 브로커의 IP 주소와 포트 번호 알아내기
    
    let broker = "192.168.180.135"; // 브로커의 IP 주소
	let port = 9001 // mosquitto를 웹소켓으로 접속할 포트 번호

	// id가 message인 DIV 객체에 브로커의 IP와 포트 번호 출력
    console.log(broker);
    console.log(port);
	
	// MQTT 메시지 전송 기능을 모두 가징 Paho client 객체 생성
	client = new Paho.MQTT.Client(broker, Number(port), CLIENT_ID);

	// client 객체에 콜백 함수 등록 및 연결
	client.onConnectionLost = onConnectionLost; // 접속 끊김 시 onConnectLost() 실행 
	client.onMessageArrived = onMessageArrived; // 메시지 도착 시 onMessageArrived() 실행
	
	// client 객체에게 브로커에 접속 지시
	client.connect({
		onSuccess:onConnect, // 브로커로부터 접속 응답 시 onConnect() 실행
	});
}

// 브로커로의 접속이 성공할 때 호출되는 함수
function onConnect() {
	console.log("접속성공");
	connectionFlag = true; // 연결 상태로 설정
}

function subscribe(topic) {
	if(connectionFlag != true) { // 연결되지 않은 경우
		alert("연결되지 않았음");
		return false;
	}
	// 구독 신청하였음을 <div> 영역에 출력
	console.log(topic+"구독 신청")
	client.subscribe(topic); // 브로커에 구독 신청
}

// 구독 한꺼번에 시키는 함수
function subscribes() {
    subscribe("dataCountPerson");
    subscribe("dataCountBath");
    subscribe("dataNowPerson");
    subscribe("dataBathNow");
    subscribe("dataCleaning");
}

function publish(topic, msg) {
	if(connectionFlag != true) { // 연결되지 않은 경우
		alert("연결되지 않았음");
		return false;
	}
	client.send(topic, msg, 0, false);
	return true;
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) { // responseObject는 응답 패킷
	if (responseObject.errorCode !== 0) {
        console.log("오류! 접속끊어짐");
        console.log(responseObject.errorCode);
	}
	connectionFlag = false; // 연결 되지 않은 상태로 설정
}

function onMessageArrived(msg) { // 매개변수 msg는 도착한 MQTT 메시지를 담고 있는 객체
	console.log("onMessageArrived: " + msg.payloadString);
    console.log("topicName: " + msg.destinationName);
    Topic = msg.destinationName;
    Message = msg.payloadString;
    changeText();
}

function changeText() {
    if(Topic == "dataCountPerson") {
        console.log(Message);
        document.getElementById("count_person").innerText = "당일 이용자 수: " + Message;
        //document.getElementById("count_person").innerHTML += '<span>당일 이용자 수: ' + Message + '</span><br/>';
        //dataCountPersonId.innerHTML = "당일 이용자: "+ Message;
    }

    if(Topic == "dataCountBath") {
        console.log(Message);
        document.getElementById("count_bath").innerText = "당일 변기 이용 수: " + Message;
        //document.getElementById("count_bath").innerHTML += '<span>당일 변기 이용 수: ' + Message + '</span><br/>';
        //dataCountBathId.innerText = "당일 변기사용: "+ Message;
    }

    if(Topic == "dataNowPerson") {
        console.log(Message);
        document.getElementById("now_person").innerText = "현재 이용자 수: " + Message;
        //document.getElementById("now_person").innerHTML += '<span>현재 이용자 수: ' + Message + '</span><br/>';
        //dataNowPerson.innerText = "현재 인원: " + Message;
    }

    if(Topic == "dataBathNow") {
        console.log(Message);
        document.getElementById("bath_now").innerText = "변기 이용자 수: " + Message;
        //document.getElementById("bath_now").innerHTML += '<span>변기 이용자 수: ' + Message + '</span><br/>';
    }

    if(Topic == "dataCleaning") {
        console.log(Message);
        document.getElementById("check_cleaning").innerText = "최근청소 일자: " + check_cleaning;
        check_cleaning = Message;
    }
}

function checkClean() {
    const today = new Date();//오늘
    publish("check_cleaning", today.toISOString().substring(0,10));
}