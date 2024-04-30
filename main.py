# Flask
from flask import Flask, request, session, render_template, jsonify, send_file, redirect, url_for
# PDF
from fpdf import FPDF
# OpenAI
from openai import OpenAI
# MongoDB
from pymongo import ReturnDocument
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
uri = os.environ.get("MONGODB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.temp

# main
@app.route("/")
def index():
    # 세션에서 로그인 상태 확인
    if 'user_id' in session:
        logged_in = True
        user = db.users.find_one({'id':session.get('user_id')})
        grade = user.get('grade')
        grade_emoji = get_emoji(grade)
        grade_title = get_title(grade)
        return render_template("main.html", logged_in=logged_in, nickname = user.get('nickname'), emoji=grade_emoji, title=grade_title)
    else:
        logged_in = False
        print(logged_in)
        return render_template("intro.html", logged_in=logged_in)
    
# emoji
def get_emoji(grade):
    emoji_dict = {
        0: "👶",
        1: "🙂",
        2: "🧑‍💻",
        10: "🧙",
        11: "👼",
        12: "🧑‍🚀",
        13: "🕵️",
        99: "🧚‍♂️"
    }
    return emoji_dict.get(grade, "❓")

# title
def get_title(grade):
    title_dict = {
        0: "Newbe",
        1: "Citizen",
        2: "Author",
        10: "Sorcerer",
        11: "Cupid",
        12: "Astronaut",
        13: "Detective",
        99: "Admin"
    }
    return title_dict.get(grade, "?")


# mypage
@app.route("/mypage")
def mypage():
    # 세션에서 로그인 상태 확인
    if 'user_id' in session:
        logged_in = True
        user = db.users.find_one({'id':session.get('user_id')})
        grade = user.get('grade')
        grade_emoji = get_emoji(grade)
        grade_title = get_title(grade)
        fantasy_cnt = user.get('fantasy_cnt')
        mystery_cnt = user.get('mystery_cnt')
        rommance_cnt = user.get('rommance_cnt')
        sf_cnt = user.get('sf_cnt')
        all_cnt = fantasy_cnt+mystery_cnt+rommance_cnt+sf_cnt

        # 페이지네이션을 위한 설정
        page = int(request.args.get('page', 1))
        per_page = 10
        total = db.novels.count_documents({'id': user.get('id')})
        posts = db.novels.find({'id': user.get('id')}).skip((page - 1) * per_page).limit(per_page)
        total_pages = (total + per_page - 1) // per_page

        return render_template("mypage.html", logged_in=logged_in, nickname=user.get('nickname'), 
                               emoji=grade_emoji, title=grade_title, 
                               fantasy_cnt=fantasy_cnt, mystery_cnt=mystery_cnt, rommance_cnt=rommance_cnt, sf_cnt=sf_cnt, 
                               all_cnt=all_cnt, posts=posts, current_page=page, total_pages=total_pages)
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
        db.users.insert_one({
            "id":userId,"pw":pw_hash,"nickname":nickname,"input_date":datetime.datetime.now(),
            "role":"USER", "grade":0,"cnt":0,
            "fantasy_cnt":0,"mystery_cnt":0,"rommance_cnt":0,"sf_cnt":0})
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

    # API 호출
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

    # DB
    user = db.users.find_one({'id':session.get('user_id')})

    text = chat_completion.choices[0].message.content
    lines = text.split('\n')

    # title
    title = lines[0].split(': ')[1]

    # text
    content = '\n'.join(lines[1:]).strip()

    # 시퀀스 생성
    postid = get_next_sequence('postId')

    db.novels.insert_one({"postId":postid,"id":user.get("id"), "nickname":user.get("nickname"), "cheracter":name,"genre":genre, "title":title ,"text":content ,"date":datetime.datetime.now()})
    
    db_genre_cnt = get_genre_cnt(genre)
    genre_cnt = user.get(db_genre_cnt) + 1
    db.users.update_one({"id":user.get("id")},{'$set': {db_genre_cnt: genre_cnt}})

    return jsonify({"title":title ,"text": content})

# 시퀀스 증가 함수
def get_next_sequence(sequence_name):
    sequence_document = db.novels.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"seq": 1}},
        projection={"seq": True, "_id": False},
        return_document=ReturnDocument.AFTER,
        upsert=True
    )
    return sequence_document['seq']
    

# DB 카운트 용도
def get_genre_cnt(genre):
    genre_dict = {
        "Romance":"rommance_cnt",
        "Fantasy":"fantasy_cnt",
        "SF":"sf_cnt",
        "Mystery":"mystery_cnt"
    }
    return genre_dict.get(genre)


# PDF 다운로드 기능
logging.basicConfig(level=logging.DEBUG)

@app.route("/download", methods=['POST'])
def download_pdf():
    try:
        text = request.form['text']
        title = request.form['title']
        pdf = FPDF()
        pdf.add_page()
        # title
        pdf.set_font("Helvetica", 'B', size=12)
        pdf.cell(200, 10, title, ln=True, align='C') 
        # 제목과 내용 사이 공백
        pdf.ln(20)
        # text
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
