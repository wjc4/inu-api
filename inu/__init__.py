import os
import logging
import sys
from flask import Flask
application = Flask(__name__)
from .db import *

db = DBConnection()

import inu.routes.square
# import inu.routes.hardcode
import inu.routes.login


# if 'DYNO' in os.environ:
#     logFormatter = logging.Formatter("%(asctime)s [%(filename)s] [%(funcName)s] [%(lineno)d] [%(levelname)-5.5s]  %(message)s")
#     specialHandler = logging.StreamHandler(sys.stdout)
#     specialHandler.setFormatter(logFormatter)
#     application.logger.addHandler(specialHandler)
#     # app.logger.addHandler(logging.StreamHandler(sys.stdout))
#     application.logger.setLevel(logging.INFO)

