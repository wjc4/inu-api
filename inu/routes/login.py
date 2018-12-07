# import logging

from flask import request, jsonify

from inu import application as app
from inu import db

import io
from PIL import Image
import time

# logger = logging.getLogger(__name__)

@app.route('/login', methods=['POST'])
def receive_image():
    # data = request.get_data()
    # print("rekt")
    # print(data)

    names = list(request.files.keys())
    for name in names:
        #first receive the file from the raspi
        print('received')
        fileImg  = request.files[name].read()
        filename = request.files[name].filename
        print(type(fileImg))
        print(fileImg)
        im = Image.open(io.BytesIO(fileImg))
        try:
            im.verify()
            print('Valid image')
        except Exception:
            print('Invalid image')
        if im.format == 'JPEG':
            print('JPEG image')
        else:
            print('Invalid image type')
        # nameSaved = './static/' + str(time.time()).replace('.', '')[-3:] + filename
        # im.save(nameSaved)

    return jsonify({"message": "hi"})


