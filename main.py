# Flask
from flask import Flask, request, render_template, jsonify, send_file
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

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# DB 연결부
uri = "mongodb+srv://andrew787a:1234@cluster0.dvmxbxe.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.temp

# main
@app.route("/")
def index():
    return render_template("main.html")

# 회원가입 기능
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    userId = data.get("userId")
    pw = data.get("password")
    nickname = data.get("nickname")

    # print(userId,pw,nickname)

    db.users.insert_one({"userId":userId,"pw":pw,"nickname":nickname,"date":datetime.datetime.now()})

    return jsonify({"message": "Registration successful!"})

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

    # db.snc.insert_one({"name":name,"genre":genre,"text":text,"date":datetime.datetime.now()})

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