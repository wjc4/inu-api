# import the necessary packages
from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
from sklearn.metrics.pairwise import paired_euclidean_distances as diff
from scipy.spatial import distance


shape_pred = './shape_predictor_68_face_landmarks.dat'

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_pred)


def get_features(image):

	image = imutils.resize(image, width=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# detect faces in the grayscale image
	rects = detector(gray, 1)

	# loop over the face detections
	for (i, rect) in enumerate(rects):
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		return shape


def check_similarity(ref, img, thresh):
	mat = diff(ref,img)
	score = np.sum(mat ** 2)
	return score < thresh

def check_mouth_open(ref, img, thresh=1.2):
	refmouth = ref[46:68]
	vert_ref = refmouth[:, 1]
	ref_dist = np.amax(vert_ref) - np.amin(vert_ref)
	threshold = thresh * ref_dist


	mouth = img[46:68]
	vertical = mouth[:, 1]
	ver_dist = np.amax(vertical) - np.amin(vertical)
	return ver_dist > threshold

def find_centroid(lm, start, end):
	points = lm[start:end]
	center = points.mean(axis=0).astype("int")
	return center[0], center[1]

def tilt_head_check(ref, img):
	ref_ratio = tilt_analysis(ref)
	img_ratio = tilt_analysis(img)
	print(img_ratio / ref_ratio)
	return img_ratio / ref_ratio > 1.2

def tilt_analysis(img):
	left_eye = find_centroid(img, 22, 27)
	right_eye = find_centroid(img, 36, 42)
	eye_center = [(left_eye[0] + right_eye[0])/2 , (left_eye[1] + right_eye[1]) /2 ]
	nose = find_centroid(img, 27, 35)
	jaw = find_centroid(img, 0, 17)
	nose2jaw = distance.euclidean(nose, jaw)
	eye2nose = distance.euclidean(eye_center, nose)
	return nose2jaw / eye2nose
	# find eye center
	#compare eye center with nose distance
	#compare
if __name__ == '__main__':
	ref_path = './reference2.jpg'
	img_path = './example.jpg'
	next_path = './mouth_open.jpg'

	image = cv2.imread(ref_path)
	image2 = cv2.imread(next_path)

	#get the landmark features as the coordinates
	img = np.asarray(get_features(image))
	img2 = np.asarray(get_features(image2))

	#specify threshold for
	#checks euclidean distance
	diff_mat = check_similarity(img, img2, thresh=20000)

	#checks if mouth is open
	check = check_mouth_open(img, img2)
	print(check)

	check = tilt_head_check(img, img2)
