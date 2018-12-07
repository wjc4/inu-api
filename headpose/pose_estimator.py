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
	print("Euclidean distance is: ", score)
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
