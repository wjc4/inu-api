import httplib, urllib, base64
import json
import io

''' to save in database: 
	personId, name, persistedFaceId (use this to remove face added to person) 
'''

headers = {
	# Request headers
	'Content-Type': 'application/json',
	'Ocp-Apim-Subscription-Key': 'caa064caa43e46df93091eb67357edba',
}

params = urllib.urlencode({})

##### CREATE PERSON GROUP, GET PERSONID #####
def create_person_group(name, personGroupId):
	body = {
		"name": name,
		"userData":"nothing"
	}

	try:
		conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
		conn.request("PUT", "/face/v1.0/persongroups/"+personGroupId+"?"+params, str(body), headers)
		response = conn.getresponse()
		data = response.read()
		print('created person group: {}'.format(personGroupId))
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))


def create_person(name, personGroupId='inuvators'):
	body = {
		"name": name,
		"userData":"nothing"
	}

	try:
		conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
		conn.request("POST", "/face/v1.0/persongroups/"+personGroupId+"/persons?"+params, str(body), headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

	json_data = json.loads(data)
	personId = json_data['personId']
	return personId

def delete_person_group(personGroupId):
	body = {}
	try:
	    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
	    conn.request("DELETE", "/face/v1.0/persongroups/"+personGroupId+"?"+params, str(body), headers)
	    response = conn.getresponse()
	    data = response.read()
	    print(data)
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

def delete_person(personId, personGroupId):
	body = {}
	try:
	    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
	    conn.request("DELETE", "/face/v1.0/persongroups/"+personGroupId+"/persons/"+personId+"?"+params, str(body), headers)
	    response = conn.getresponse()
	    data = response.read()
	    print(data)
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))


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
	conn.request("POST", "/face/v1.0/persongroups/"+personGroupId+"/persons/"+personId+"/persistedFaces?"+addface_params, body, headers)
	response = conn.getresponse()
	data = response.read()
	print('added face:\n'+str(data))
	conn.close()

	return True


##### CHECK IF PHOTO CONTAINS PERSON #####
# Use Detect to get faceIds of faces in each photo, call Verify.
# returns detection_status, face_attributes (if verified)
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
		'returnFaceAttributes': 'emotion'
	})

	body = image_data

	conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
	conn.request("POST", "/face/v1.0/detect?"+params, body, headers)
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

# Face to person recognition.
def check_face(faceId, personId, personGroupId):
	headers = {
		# Request headers
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': 'caa064caa43e46df93091eb67357edba',
	}

	body = {
		'faceId': faceId,
		'personId': personId,
		'personGroupId': personGroupId
	}

	conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
	conn.request("POST", "/face/v1.0/verify?"+params, str(body), headers)
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
	personGroupId = "inuvators"
	personGroupName = "Inuvators"
	name = "De Sheng"

	create_person_group(personGroupName, personGroupId) # create the group inuvators
	personId = create_person(name, personGroupId) # create the person. This personId needs to be saved into DB.
	
	personId = 'a97bf5e8-1e67-4970-a37a-a3be941fee96' # derp
	# register a face under the personId
	with open("derp.jpg", "rb") as imageFile:
		f = imageFile.read()
		b = bytearray(f)
	add_face(b, personId, personGroupId)

	# import time
	# from PIL import Image
	# img = Image.open('jx2.jpg')
	# basewidth = 200
	# wpercent = (basewidth/float(img.size[0]))
	# hsize = int((float(img.size[1])*float(wpercent)))
	# img = img.resize((basewidth,hsize), Image.ANTIALIAS)
	# # img.save('sompic.jpg') 
	# with io.BytesIO() as output:
	#     img.save(output, 'BMP')
	#     b = output.getvalue()
	with open("jx.jpg", "rb") as imageFile:
		f = imageFile.read()
		b = bytearray(f)
	# s = time.time()
	correct, face_attributes = check_image(b, personId, personGroupId)
	# e = time.time()
	# print(e-s)

	# delete_person(personId, personGroupId)
	# delete_person_group(personGroupId)

if __name__ == '__main__':
	main()