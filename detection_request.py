import cv2
import requests
import numpy as np

api_endpoint = "http://127.0.0.1:5000/detect_faces" 

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame,(200,200))
    
    if ret:
        cv2.imshow('Live Video Feed', frame)
        _, frame_encoded = cv2.imencode('.jpg', frame)
        frame_bytes = frame_encoded.tobytes()
        
        headers = {
            "Content-Type": "image/jpeg"
        }
        response = requests.post(api_endpoint, data=frame_bytes, headers=headers)
        
        if response.status_code == 200:
            print(response.json())
        else:
            print("Error sending frame. Status code:", response.status_code)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break
    else:
        print("Error reading frame from the camera.")
        break

cap.release()
cv2.destroyAllWindows()