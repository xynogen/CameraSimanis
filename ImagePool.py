import firebase_admin
from firebase_admin import credentials, db, storage

from dotenv import load_dotenv
import os

import requests
import cv2
import numpy as np

import time
import datetime


# load .env to enviromemt variable
load_dotenv()
API_KEY = os.environ['API_KEY']

HOST_CAMERA = os.environ['HOST_CAMERA']
PORT_CAMERA = os.environ['PORT_CAMERA']
URL = f'http://{HOST_CAMERA}:{PORT_CAMERA}/api/camera/capture?api_key={API_KEY}'

FIREBASE_CRED_FILE = os.environ['FIREBASE_CRED_FILE']
FIREBASE_BUCKET = os.environ['FIREBASE_BUCKET']
FIREBASE_URL = os.environ['FIREBASE_URL']

TEMP_FOLDER = os.environ['TEMP_FOLDER']

DEBUG = os.environ['DEBUG']
INTERVAL = os.environ['INTERVAL']
INTERVAL = int(INTERVAL)


cred = credentials.Certificate(FIREBASE_CRED_FILE)
firebase_app = firebase_admin.initialize_app(cred, {"storageBucket": FIREBASE_BUCKET})
ref = db.reference(url=FIREBASE_URL, app=firebase_app)

while True:
    response = requests.get(URL, stream=True).raw
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    process = True
    try:
        img_H = image.shape[0]
        img_W = image.shape[1]
    except:
        print('[Warning] Cannot Reach to Camera')
        process = False


    # for testing
    if DEBUG == 'true':
        def get_mouse_position(event,x,y,flags,param):
            global mouseX,mouseY
            if event == cv2.EVENT_LBUTTONDBLCLK:
                mouseX,mouseY = x,y
                print(f'Mouse X : {mouseX}')
                print(f'Mouse Y : {mouseY}')

            
        cv2.imshow('image', image)
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', get_mouse_position)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if process:
        FILENAME = 'Sungai.jpg'
        FILEPATH = f'./{TEMP_FOLDER}/{FILENAME}'
        status = cv2.imwrite(FILEPATH, image)

        if not status:
            print('[Warning] Failed to Write Image') 

        bucket = storage.bucket(app=firebase_app)
        blob = bucket.blob(FILENAME)
        blob.upload_from_filename(FILEPATH)

        counter = ref.child('data_counter').get()
        counter = int(counter) +1 
        counter = str(counter)
        ref.child('data_counter').set(counter)
        print("[INFO] Image Has Been Uploaded")


    time.sleep(INTERVAL)
