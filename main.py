# Flask
from flask import Flask, request, render_template, jsonify, send_file
# PDF
from fpdf import FPDF

import os
# OpenAI
from openai import OpenAI

# MongoDB
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import tempfile
import logging

app = Flask(__name__)

uri = "mongodb+srv://andrew787a:----@cluster0.dvmxbxe.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.temp

@app.route("/")
def index():
    return render_template("main.html")

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

    db.snc.insert_one({"name":name,"genre":genre,"text":text})

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