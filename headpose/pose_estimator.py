# import the necessary packages
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
from PIL import Image



img_path = './example.jpg'
shape_pred = './shape_predictor_68_face_landmarks.dat'


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_pred)

# load the input image, resize it, and convert it to grayscale
image = Image.open(img_path)
width, height = image.size

image = cv2.imread(img_path)

image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect faces in the grayscale image
rects = detector(gray, 1)
blank_image = np.zeros((500,500,3), np.uint8)

# loop over the face detections
for (i, rect) in enumerate(rects):
	# determine the facial landmarks for the face region, then
	# convert the facial landmark (x, y)-coordinates to a NumPy
	# array
	shape = predictor(gray, rect)
	shape = face_utils.shape_to_np(shape)
	print(shape)

	# loop over the (x, y)-coordinates for the facial landmarks
	# and draw them on the image
	for (x, y) in shape:
		cv2.circle(blank_image, (x, y), 1, (0, 0, 255), -1)

# show the output image with the face detections + facial landmarks
#cv2.imshow("Output", blank_image)
cv2.waitKey(0)
