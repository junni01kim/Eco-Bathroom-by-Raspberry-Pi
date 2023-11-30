#5. 플라스크를 만든다.
import datetime
import PublicBathroom
from flask import Flask, render_template, request
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#5-1. 현재 인원, 당일 사용자 수, 현재 변기 인원, 당일 변기 이용자 수, 청소 체크 버튼, 로그 보기 버튼
@app.route('/')
def selectNow():
    now  = datetime.datetime.now()
    nowString = now.strftime("%Y-%m-%d")

    return render_template('Now.html', date = nowString)

    #5-2. 로그 보기 버튼을 누르면 최근 청소날짜를 출력하고 전체 기록과 값의 평균치를 출력한다.
@app.route('/view/')
def selectView():
    PublicBathroom.get_day_of_user_data(PublicBathroom.day_of_user_data)
    # 의문
    return render_template('View.html', dict = PublicBathroom.day_of_user_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)