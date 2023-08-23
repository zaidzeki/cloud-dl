#!/usr/bin/env python3

import base64
import requests

from flask import Flask, render_template, request, jsonify, Response
from pytube import YouTube
from humanfriendly import module as humanfriendly

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET'] = 'sfljksnfljgnlaekjpqoaljhuyugtfresddxdfcgvhbjnkml'

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

@app.route('/details', methods=['POST'])
def details():
    url = request.form.get('url')
    try:
        video = YouTube(url)
        streams = video.streams.filter(adaptive=True).all()
        streams += video.streams.filter(only_audio=True).all()
        streams = [{
            'video': stream.includes_video_track,
            'filesize': humanfriendly.format_size(stream.filesize),
            'itag': stream.itag,
            'bitrate': humanfriendly.format_size(stream.bitrate),
            'format': stream.subtype,
            'type': stream.type,
            'resolution': stream.resolution if stream.includes_video_track else 'audio'
        } for stream in streams]
        return success(streams)
    except Exception as e:
        return error(str(e))

@app.route('/download', methods=['POST'])
def download():
    url = int(request.form.get('url'))
    itag = int(request.form.get('itag'))
    video = YouTube(url)
    video_url = video.get_by_itag(itag).url
    encoded_url = '/proxy/'+str(base64.urlsafe_b64encode(bytes(video_url, 'utf-8')), 'utf-8')
    return success(encoded_url)


@app.route('/proxy/<encoded>')
def proxy(encoded):
    decoded = base64.urlsafe_b64decode(bytes(encoded, 'utf-8'))
    decoded = str(decoded, 'utf-8')
    resp = requests.get(decoded)
    return Response(resp.iter_content(512*1024))


app.run()
