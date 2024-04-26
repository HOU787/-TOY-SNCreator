# Flask
from flask import Flask, request, session, render_template, jsonify, send_file, redirect, url_for
# PDF
from fpdf import FPDF
# OpenAI
from openai import OpenAI
# MongoDB
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
import datetime
import tempfile
import logging

# 암호화
import jwt
import hashlib

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'NOWEVERYONECANAUTHOR'

# DB 연결부
uri = "mongodb+srv://andrew787a:1234@cluster0.dvmxbxe.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.temp

# main
@app.route("/")
def index():
    # 세션에서 로그인 상태 확인
    if 'user_id' in session:
        logged_in = True
        user = db.users.find_one({'id':session.get('user_id')})
        return render_template("main.html", logged_in=logged_in, nickname = user.get('nickname'))
    else:
        logged_in = False
        print(logged_in)
        return render_template("intro.html", logged_in=logged_in)

# 회원가입 기능
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    userId = data.get("userId")
    pw = data.get("password")
    nickname = data.get("nickname")
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    # 이미 존재하는 아이디 or 닉네임 검증

    result1 = db.users.find_one({'id': userId})
    result2 = db.users.find_one({'nickname':nickname})

    if result1 is not None:
        return jsonify({'result': 'fail','message': 'ID already exist'})
    elif  result2 is not None:
        return jsonify({'result': 'fail','message': 'Nickname already exist'})
    else:
        db.users.insert_one({"id":userId,"pw":pw_hash,"nickname":nickname,"input_date":datetime.datetime.now()})
        return jsonify({'result': 'success',"message": "Registration successful!"})

# 로그인 기능
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # 클라이언트에서 보낸 JSON 데이터를 가져옴
    userId = data.get("userId")
    password = data.get("password")
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()  # 비밀번호 해싱

    # DB에서 유저 정보 찾기
    result = db.users.find_one({"id": userId, "pw": pw_hash})
    if result is not None:
        session['user_id'] = userId  # 세션에 사용자 ID 저장
        return jsonify({'result': 'success', 'message': 'Login successful!'})
    else:
        return jsonify({'result': 'fail', 'message': 'Invalid ID or password'})

# 로그아웃 기능
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # 세션에서 사용자 ID 제거
    return redirect(url_for('index'))

# ChatGPT API 이용, 단편소설 생성 기능
@app.route("/", methods=['POST'])
def write():
    name = request.form.get("nickname")
    genre = request.form.get("genre")

    send_message = f"You are an author. write a novel in 3000 characters under the main character name: {name}, Genre: {genre}. and you must write title"

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": send_message}
        ],
        model="gpt-3.5-turbo",
    )

    text = chat_completion.choices[0].message.content

    db.snc.insert_one({"name":name,"genre":genre,"text":text,"date":datetime.datetime.now()})

    return jsonify({"text": text})


# PDF 다운로드 기능
logging.basicConfig(level=logging.DEBUG)

@app.route("/download", methods=['POST'])
def download_pdf():
    try:
        text = request.form['text']
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=9)
        pdf.multi_cell(0, 10, text)
        
        pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(pdf_output.name)
        pdf_output.close()

        return send_file(pdf_output.name, as_attachment=True, mimetype='application/pdf', download_name="Your_Story.pdf")
    except Exception as e:
        logging.error(f"Error generating PDF: {e}")
        return "An error occurred", 500

if __name__ == "__main__":
    app.run(debug=True)