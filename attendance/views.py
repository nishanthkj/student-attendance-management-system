from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import os
import cv2
import face_recognition
import numpy as np
from .models import Student, Log
from .forms import StudentForm
from datetime import datetime

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encode = encodings[0]
            encodeList.append(encode)
    return encodeList

def load_students():
    path = 'attendance/Training_images'
    if not os.path.exists(path):
        return  # Path does not exist, handle accordingly
    my_list = os.listdir(path)
    images = []
    classNames = []
    for cl in my_list:
        cur_img = cv2.imread(f'{path}/{cl}')
        images.append(cur_img)
        classNames.append(os.path.splitext(cl)[0])
    encodeListKnown = findEncodings(images)
    for encode, name in zip(encodeListKnown, classNames):
        Student.objects.update_or_create(usn=name, defaults={'face_embedding': encode.tobytes()})
def index_view(request):
    return render(request, 'attendance/index.html')

def login_view(request):
    return render(request, 'attendance/login.html')

def attendance_view(request):
    return render(request, 'attendance/attendance.html')

def dash_view(request):
    return render(request, 'attendance/dash.html')

def add_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            
            # Process the uploaded image to get the face encoding
            image = request.FILES['studentImage']
            img = face_recognition.load_image_file(image)
            encodings = face_recognition.face_encodings(img)
            
            if len(encodings) > 0:
                student.face_embedding = encodings[0].tobytes()
                student.image = image  # Save the image file
            student.save()
            return redirect('dash')
    else:
        form = StudentForm()
    
    return render(request, 'attendance/add.html', {'form': form})

def mark_attendance(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        student = get_object_or_404(Student, usn=usn)
        Log.objects.create(student=student, timestamp=datetime.now())
        return JsonResponse({'message': 'Attendance marked successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def view_students(request):
    students = Student.objects.all()
    return render(request, 'attendance/view_students.html', {'students': students})

load_students()  # Load students once on server start
