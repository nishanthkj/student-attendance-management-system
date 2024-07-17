<<<<<<< HEAD
from flask import Flask, render_template, jsonify, request, redirect, url_for
=======
from flask import Flask, render_template, jsonify, request
>>>>>>> 9f3a95a5ede23d62d5e02e4feb7ef97bd3c15e91
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

app = Flask(__name__)

# Function to find encodings
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Function to mark attendance
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# Initialize variables and load images
path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Route for marking attendance via API endpoint
@app.route('/mark-attendance', methods=['POST'])
def mark_attendance():
    # Receive data from frontend
    data = request.get_json()
    name = data['name']

    # Perform face recognition and mark attendance
<<<<<<< HEAD
=======
    # (This part should be similar to your existing while loop logic)
>>>>>>> 9f3a95a5ede23d62d5e02e4feb7ef97bd3c15e91
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

    return jsonify({'message': 'Attendance marked successfully'})

<<<<<<< HEAD
# Route to serve the login page
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/attendance')
def attendance():
    return render_template('attendance.html')
# Route to serve the index page
=======
# Route to serve the HTML page
>>>>>>> 9f3a95a5ede23d62d5e02e4feb7ef97bd3c15e91
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
