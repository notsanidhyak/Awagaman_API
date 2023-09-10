import requests
import cv2

api_endpoint = "http://127.0.0.1:5000/encode_face"

text_data = 'Adam'

img_data = cv2.imread('face_data/Adam.jpeg')
img_bytes = cv2.imencode('.jpg', img_data)[1].tobytes()

data = {
    'text': text_data,
}

files = {
    'image': ('image.jpg', img_bytes, 'image/jpeg')  # Adjust the MIME type as needed.
}

response = requests.post(api_endpoint, data=data, files=files)
if response.status_code == 200:
    print(response.json())
else:
    print("Error sending frame. Status code:", response.status_code)