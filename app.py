from flask import Flask, request, jsonify
import cv2
import face_recognition
import json
import numpy as np

app = Flask(__name__)

frame_buffer = []

en_file_path = "encoding_list.json"
with open(en_file_path, 'r') as json_file:
    images_encoding = json.load(json_file)

print(images_encoding)

nm_file_path = "name_list.json"
with open(nm_file_path, 'r') as json_file:
    images_names = json.load(json_file)


@app.route('/',methods=['GET'])
def home():
    return jsonify(['Awagaman is alive and running perfectly!'])


@app.route('/encode_face', methods=['POST'])
def encode_face():
    global images_encoding
    global images_names

    if 'image' not in request.files:
        return jsonify(['No image file provided'])
    
    if 'text' not in request.form:
        return jsonify(['No text provided'])

    img_data = request.files['image']
    text_data = request.form['text']

    img_bytes = img_data.read()
    img_np = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(images_encoding)
    images_encoding.append((face_recognition.face_encodings(rgb_img)[0]).tolist())
    images_names.append(text_data)

    print("yolo")
    with open(en_file_path, 'w') as json_file:
        json.dump(images_encoding, json_file)

    with open(nm_file_path, 'w') as json_file:
        json.dump(images_names, json_file)

    return jsonify(['Image and Text: Received and Encoded'])


@app.route('/detect_faces', methods=['POST'])
def detect_faces():
    global frame_buffer

    video_stream = request.stream
    frameinbinary = b''

    while True:
        chunk = video_stream.read(1024)
        if not chunk:
            break
        frameinbinary += chunk

        frame_data_np = np.frombuffer(frameinbinary, dtype=np.uint8)
        frameflip = cv2.imdecode(frame_data_np, cv2.IMREAD_COLOR)
        frame = cv2.flip(frameflip,1)
        frame = cv2.resize(frame,(180,180))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        curr_face_locations = face_recognition.face_locations(rgb_frame)
        # detected_face_locations = np.array(curr_face_locations)
        curr_face_encodings = face_recognition.face_encodings(frame,curr_face_locations)

        detected_face_names = []

        for i in curr_face_encodings:
            curr_name = "Unknown"
            distances = face_recognition.face_distance(images_encoding, i)
            result = list(distances <= 0.55)

            if True in result:
                matches = face_recognition.compare_faces(images_encoding, i)
                face_distances = face_recognition.face_distance(images_encoding, i)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    curr_name = images_names[best_match_index]
                detected_face_names.append(curr_name)
                # print(detected_face_names)
            else:
                detected_face_names.append(curr_name)
                # print(detected_face_names)

    if not detected_face_names:
        return jsonify(["No faces found"])
    else:
        print(detected_face_names)
        return jsonify(detected_face_names)

if __name__ == '__main__':
    app.config['ENV'] = 'production'  # Set Flask to production mode
    app.run()