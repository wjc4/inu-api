import httplib, urllib, base64
import json
import io

''' to save in database: 
	personId, name, userData, personGroupId, persistedFaceId (use this to remove face added to person) 
'''


##### CREATE PERSON GROUP, GET PERSONID #####
def create_person(name, personGroupId):
	headers = {
		# Request headers
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': 'caa064caa43e46df93091eb67357edba',
	}

	create_params = urllib.urlencode({
		'personGroupId': personGroupId
	})

	body = {
		"name": name,
		"userData":"nothing"
	}

	conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
	conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons?%s" % create_params, str(body), headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	print('created person:\n'+str(data))

	json_data = json.loads(data)
	personId = json_data['personId']
	return personId

def add_face(image_data, personId, personGroupId):
	headers = {
		# Request headers
		'Content-Type': 'application/octet-stream',
		'Ocp-Apim-Subscription-Key': 'caa064caa43e46df93091eb67357edba',
		'Process-Data': False
	}

	addface_params = urllib.urlencode({
		# Request parameters
		'personGroupId': personGroupId,
		'personId': personId
	})

	body = image_data

	conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
	conn.request("POST", "/face/v1.0/persongroups/{personGroupId}/persons/{personId}/persistedFaces?%s" % addface_params, str(body), headers)
	response = conn.getresponse()
	data = response.read()
	print('added face:\n'+str(data))
	conn.close()

	return True


##### CHECK IF PHOTO CONTAINS PERSON #####
# Use Detect to get faceIds of faces in each photo, call Verify.
# If verified, then use result from Detect to get location
# returns detection_status, fearfulness
def check_image(image_data, personId, personGroupId):
	headers = {
		# Request headers
		'Content-Type': 'application/octet-stream',
		'Ocp-Apim-Subscription-Key': 'caa064caa43e46df93091eb67357edba',
		'Process-Data': False
	}

	params = urllib.urlencode({
		# Request parameters
		'returnFaceId': 'true',
		'returnFaceLandmarks': 'false',
	})

	body = image_data


	conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
	conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
	response = conn.getresponse()
	data = response.read()
	print('checked photo:\n'+str(data))
	conn.close()

	json_data = json.loads(data)
	for entry in json_data:
		faceId = str(entry['faceId'])
		if check_face(faceId, personId, personGroupId):
			# coords = entry['faceRectangle']
			# return (coords['top'], coords['left'], coords['width'], coords['height'])
			return (True, entry['faceAttributes'])
	else:
		return (False, None)

def check_face(faceId, personId, personGroupId):
	headers = {
		# Request headers
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': 'caa064caa43e46df93091eb67357edba',
	}


	params = urllib.urlencode({
	})

	body = {
		'faceId': faceId,
		'personId': personId,
		'personGroupId': personGroupId
	}

	conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
	conn.request("POST", "/face/v1.0/verify?%s" % params, str(body), headers)
	response = conn.getresponse()
	data = response.read()
	print('checked face:\n'+str(data))
	conn.close()

	json_data = json.loads(data)
	if json_data['isIdentical']:
		return True
	else:
		return False

def main():
	# name = 'Vladimr Putin'
	# personGroupId = 'putin'
	# selfie = 'http://i.telegraph.co.uk/multimedia/archive/03463/putin_3463140k.jpg'
	# photo = 'https://jafrianews.files.wordpress.com/2012/05/russian-president-putin-with-vladimir-putin-may-7-2012.jpg'
	# photo = 'http://i.telegraph.co.uk/multimedia/archive/03463/putin_3463140k.jpg'


	# urllib.urlretrieve(photo, 'photo.jpg')
	with open("IMG_0641.JPG", "rb") as imageFile:
		f = imageFile.read()
		b = bytearray(f)

	'''jiarui'''
	# add_face(b, 'cd09435a-c73b-4df2-888a-31af70a8a2f1', 'jiarui')
	#b5f2f363-39c4-4f6f-80f8-2f222ee48be8 <-- persisted face that wasa wrongly added, removed alr

	'''xinchen'''
	#add_face(b, 'e49417ac-0960-4711-a6e4-be3ffaf32ab9', 'xinchen')

	'''jiexun'''
	#add_face(b, '83210ef7-0ac4-413b-8c75-3eab6beb101b', 'jiexun')
	# ee447ea5-4abe-4ff7-a363-14cba98b434b  <-- persisted face for smiling face I added

	# possible_coords = check_photo(b, 'e49417ac-0960-4711-a6e4-be3ffaf32ab9', 'xinchen')
	# print (possible_coords)
	# print ('done!')

if __name__ == '__main__':
	main()
	#check_face('30d72dba-7049-485b-9421-5a64255d195c', 'b00c6a39-7807-4cf2-9a04-6b41f2efcf18', 'putin')
