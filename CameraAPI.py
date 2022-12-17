import cv2
from flask import Flask, request, send_file, render_template
from flask_cors import CORS

import json
import uuid
import io

from dotenv import load_dotenv
import os

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# load .env
load_dotenv()

HOST_CAMERA = os.environ['HOST_CAMERA']
PORT_CAMERA = os.environ['PORT_CAMERA']
RTSP_URL = os.environ['RTSP_URL']
DB_NAME = os.environ["DB_NAME"]
DB_URI = f'sqlite:///{DB_NAME}'
DEBUG = os.environ['DEBUG']


app = Flask(__name__)
CORS(app, supports_credentials=True)
Base = declarative_base()
engine = sql.create_engine(DB_URI)

# class for defining the APIKeys Table
class APIKeys(Base):
    __tablename__ = 'api_keys'
    id = sql.Column(sql.Integer(), primary_key=True)
    api_key = sql.Column(sql.String(36))

@app.route("/", methods=['GET'])
def index():
    hostname = request.headers.get('Host')
    return render_template(
        'documentation.html',
        hostname = hostname
    ).encode(encoding='UTF-8')


@app.route('/api/camera/status', methods=['GET'])
def status():
    DBSession = sessionmaker(bind=engine)
    dbSession = DBSession()

    api_key = request.args.get("api_key")
    API_KEY = dbSession.query(APIKeys).first()

    dbSession.close()

    if api_key != API_KEY.api_key:
        return json.dumps({'message': 'API Keys Needed'})

    camera = cv2.VideoCapture(RTSP_URL)
    status, _ = camera.read()

    if status != True:
        return json.dumps({'status': 'Failed', 'message': 'Cannot Access the Camera, check the connection'})
    
    camera.release()
    return json.dumps({'status': 'Success', 'message': 'Camera Connected'})


@app.route('/api/camera/capture', methods=['GET'])
def capture():
    DBSession = sessionmaker(bind=engine)
    dbSession = DBSession()

    api_key = request.args.get("api_key")
    API_KEY = dbSession.query(APIKeys).first()

    dbSession.close()

    if api_key != API_KEY.api_key:
        return json.dumps({'message': 'API Keys Needed'})

    camera = cv2.VideoCapture(RTSP_URL)
    status, image = camera.read()

    if status != True:
        return json.dumps({'status': 'Failed', 'message': 'Cannot Access the Camera, check the connection'})

    _, buffer = cv2.imencode('.jpg', image)

    camera.release()
    image_name = uuid.uuid1()

    return send_file(
        io.BytesIO(buffer),
        mimetype='image/jpeg',
        as_attachment=False,
        download_name=f'{image_name}.jpg')


if __name__ == '__main__':
    debug = True if DEBUG == 'true' else False

    app.run('0.0.0.0', port=PORT_CAMERA, debug=debug)