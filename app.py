#!/usr/bin/env python3

import os
from glob import glob

import requests
from pytube import YouTube
from flask import Flask, jsonify, render_template, request
from humanfriendly import module as humanfriendly
from mega import Mega

mega = Mega()
m = mega.login(
    os.environ.get('MEGA_USER', ''),
    os.environ.get('MEGA_PASS', '')
)


app = Flask(__name__)
app.config['DEBUG'] = True

def success(data):
    return jsonify({
        'status': 'success',
        'data': data
    })

def error(message):
    return jsonify({
        'status': 'error',
        'message': message
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    name = request.form.get('name')
    try:
        resp = requests.get(url, stream=True, allow_redirects=True)
        for i, chunk in enumerate(resp.iter_content(100*1000*1000)):
            filename = f'static/files/{name}.{i}'
            with open(filename, 'wb') as fout:
                fout.write(chunk)
            # TODO use proper keywords
            os.chdir('static/files')
            m.upload(f'{name}.{i}')
            os.remove(f'{name}.{i}')
            os.chdir('../..')
    except Exception as e:
        return error(str(e))
    return success('')

@app.route('/list', methods=['POST'])
def list():
    files = glob('static/files/*')
    files.sort(key=lambda path: os.path.getmtime(path))
    files = [{
        'name':file,
        'size':humanfriendly.format_size(os.path.getsize(file))
        } for file in files]
    return success(files)

@app.route('/delete', methods=['POST'])
def delete():
    url = request.form.get('url')
    os.remove(url)
    if not os.path.exists(url):
        return success('')
    else:
        return error('Couldn\'t delete file')

@app.route('/links', methods=['POST'])
def links():
    url = request.form.get('url')
    try:
        video = YouTube(url)
        streams = video.streams.filter(progressive=True).all()
        streams += video.streams.filter(only_audio=True).all()
        streams = [{
            'url': stream.url,
            'resolution': stream.resolution if stream.type == 'video' else stream.abr,
            'filesize': humanfriendly.format_size(stream.filesize)
        } for stream in streams]
    except Exception as e:
        return error(str(e))
    return success(streams)

if __name__ == "__main__":
    app.run(host="::")
