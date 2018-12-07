# import logging

from flask import request, jsonify

from inu import application as app
from inu import db

from inu.faceapi import *
import inu.pose_estimator as pe

import io
from PIL import Image
import time
import numpy as np

# logger = logging.getLogger(__name__)
name = 'De Sheng'
personGroupId = 'inuvators'
personId = 'a97bf5e8-1e67-4970-a37a-a3be941fee96'
db_entry = 'inuvator'
reference_image = ''


@app.route('/image', methods=['POST'])
def receive_image():
    # data = request.get_data()
    # print("rekt")
    # print(data)

    result = db.get(db_entry)
    status = result['status']
    names = list(request.files.keys())

    valid = False
    for name in names:
        # first receive the file from the raspi
        print('received')
        fileImg = request.files[name].read()
        # filename = request.files[name].filename
        print(type(fileImg))
        # print(fileImg)
        im = Image.open(io.BytesIO(fileImg))
        
        try:
            im.verify()
            print('Valid image')
            if im.format == 'JPEG':
                # imgByteArr = io.BytesIO()
                # roiImg.save(imgByteArr, format='JPEG')
                # fileImg = imgByteArr.getvalue()
                valid = True
                print('JPEG image')
                break
            else:
                print('Invalid image type')
        except Exception:
            print('Invalid image')
        if valid:
            break
        # nameSaved = './static/' + str(time.time()).replace('.', '')[-3:] + filename
        # im.save(nameSaved)

    # im = Image.open(io.BytesIO(fileImg))
    # im = im.rotate(90)
    # imgByteArr = io.BytesIO()
    # im.save(imgByteArr, format='JPEG')
    # fileImg = imgByteArr.getvalue()

    global reference_image
    if status == 0:
        print('recognising')
        correct, face_attributes = check_image(
            fileImg, personId, personGroupId)
        if correct:
            result['status'] = 1
            db.update(db_entry, result)
            if 'emotions' in result:
                result['emotions'].append(face_attributes)
            else:
                result['emotions'] = [face_attributes]
            reference_image = fileImg
    elif status == 1:
        # do liveliness check 1
        ref_im = Image.open(io.BytesIO(reference_image))
        ref_im = ref_im.rotate(270)
        ref_lm = np.asarray(pe.get_features(ref_im))
        im = Image.open(io.BytesIO(fileImg))
        im = im.rotate(270)
        lm = np.asarray(pe.get_features(im))
        if lm is None:
            return jsonify({'status': 1})
        verify = pe.check_mouth_open(ref_lm, lm)
        if verify:
            print("Mouth open")
            result['status'] = 2
            db.update(db_entry, result)
    elif status == 2:
        # do liveliness check 2
        ref_im = Image.open(io.BytesIO(reference_image))
        ref_im = ref_im.rotate(270)
        ref_lm = np.asarray(pe.get_features(ref_im))
        im = Image.open(io.BytesIO(fileImg))
        im = im.rotate(270)
        lm = np.asarray(pe.get_features(im))
        if lm is None:
            return jsonify({'status': 2})
        verify = pe.tilt_head_check(ref_lm, lm)
        if verify:
            print("Head tilted")
            result['status'] = 3
            db.update(db_entry, result)
    return jsonify({'status': result['status']})


@app.route('/login', methods=['GET'])
def login():
    result = db.get(db_entry)
    result['status'] = 0
    db.update(db_entry, result)
    return jsonify({'status': result['status']})


@app.route('/status', methods=['GET'])
def status():
    result = db.get(db_entry)
    return jsonify({'status': result['status']})
