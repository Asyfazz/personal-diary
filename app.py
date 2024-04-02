import os
from os.path import join, dirname
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb://test:sparta@ac-xqkccln-shard-00-00.z4hmlqe.mongodb.net:27017,ac-xqkccln-shard-00-01.z4hmlqe.mongodb.net:27017,ac-xqkccln-shard-00-02.z4hmlqe.mongodb.net:27017/?ssl=true&replicaSet=atlas-11kcde-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['POST'])
def save_diary():
    # get file from client
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    file_name = f"file-{datetime.now().strftime('%Y%m%d-%H%M%S')}.{extension}"
    file.save(f"static/{file_name}")

    # get profile from client
    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1]
    profile_name = f"profile-{datetime.now().strftime('%Y%m%d-%H%M%S')}.{extension}"
    profile.save(f"static/{profile_name}")

    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    doc = {
        'file': file_name,
        'profile': profile_name,
        'title': title_receive,
        'content': content_receive,
        'created_at': datetime.now().strftime('%Y.%m.%d')
    }
    db.diarys.insert_one(doc)

    return jsonify({'msg': 'Upload complete!'})


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diarys.find({}, {'_id': False}))
    return jsonify({'articles': articles})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)