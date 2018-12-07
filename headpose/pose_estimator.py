# import the necessary packages
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
from PIL import Image
from sklearn.metrics.pairwise import paired_euclidean_distances as diff
from scipy.spatial import distance


ref_path = './reference2.jpg'
img_path = './example.jpg'
next_path = './mouth_open.jpg'
shape_pred = './shape_predictor_68_face_landmarks.dat'

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_pred)

def getFeatures(img_path):
	image = Image.open(img_path)
	width, height = image.size

	image = cv2.imread(img_path)

	image = imutils.resize(image, width=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale image
	rects = detector(gray, 1)
	print(len(rects))
	# loop over the face detections
	for (i, rect) in enumerate(rects):
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		for (x, y) in shape:
			cv2.circle(blank_image, (x, y), 1, (0, 0, 255), -1)

		return shape

def check_similarity(ref, img, thresh):
	mat = diff(ref,img)
	score = np.sum(mat ** 2)
	print(score)
	return score < thresh

def check_mouth_open(ref, img, thresh=1.4):
	refmouth = img[46:68]
	vert_ref = refmouth[:, 1]
	ref_dist = np.amax(vert_ref) - np.amin(vert_ref)
	threshold = thresh * ref_dist


	mouth = img[46:68]
	vertical = mouth[:, 1]
	ver_dist = np.amax(vertical) - np.amin(vertical)
	print(ver_dist)
	return ver_dist < threshold


if __name__ == '__main__':
	ref = np.asarray(getFeatures(ref_path))
	img = np.asarray(getFeatures(img_path))
	img2 = np.asarray(getFeatures(next_path))

	thresh = 200000
	diff_mat = check_similarity(ref, img, thresh)
	diff_mat2 = check_similarity(ref, img2, thresh)

	res = check_mouth_open(ref, img2)
	print(res)
