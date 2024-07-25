from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import os
import cv2
import face_recognition
import numpy as np
from .models import Student, Log
from .forms import StudentForm
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
import base64

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encode = encodings[0]
            encodeList.append(encode)
    return encodeList
from django.shortcuts import render

def attendance_view(request):
    # Add your logic for attendance view here
    return render(request, 'attendance/attendance.html')

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
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dash')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'attendance/login.html', {'form': form})

def mark_attendance(request):
    if request.method == 'POST':
        image_data = request.POST.get('image')
        if image_data:
            image_data = image_data.split(",")[1]
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            image = np.array(image)

            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:
                live_encoding = face_encodings[0]

                # Compare with stored embeddings
                students = Student.objects.all()
                for student in students:
                    stored_encoding = np.fromstring(student.embedding[1:-1], sep=',')
                    match = face_recognition.compare_faces([stored_encoding], live_encoding)
                    if match[0]:
                        # Mark attendance for the student
                        student.attendance_marked = True
                        student.save()
                        return JsonResponse({
                            'status': 'success',
                            'name': student.name,
                            'usn': student.usn,
                        })

            return JsonResponse({'status': 'error', 'message': 'No face detected or no match found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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

            # Create a staff user
            username = student.usn
            password = get_random_string(length=8)  # Generate a random password
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = True  # Give the user staff permissions
            user.save()

            # Optionally send the username and password to the student's email
            # You can implement email sending logic here

            return redirect('dash')
    else:
        form = StudentForm()
    
    return render(request, 'attendance/add.html', {'form': form})

def mark_attendance(request):
    if request.method == 'POST':
        data_url = request.POST.get('image')
        _, encoded = data_url.split(',', 1)
        image_data = base64.b64decode(encoded)
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                usn = known_face_usns[best_match_index]
                student = get_object_or_404(Student, usn=usn)
                Log.objects.create(student=student, timestamp=datetime.now())
                return JsonResponse({'status': 'success', 'usn': usn, 'name': student.name})
        
        return JsonResponse({'status': 'no_match'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def view_students(request):
    students = Student.objects.all()
    return render(request, 'attendance/view_students.html', {'students': students})

# Load students' encodings on server start
# load_students()
# known_face_encodings = list(Student.objects.values_list('face_embedding', flat=True))
# known_face_usns = list(Student.objects.values_list('usn', flat=True))
# known_face_encodings = [np.frombuffer(encoding, dtype=np.float64) for encoding in known_face_encodings]
def dash_view(request):
    students = Student.objects.all()
    attendance_logs = Log.objects.select_related('student').all()
    context = {
        'students': students,
        'attendance_logs': attendance_logs,
    }
    return render(request, 'attendance/dash.html', context)

def student_details_view(request, usn):
    student = get_object_or_404(Student, usn=usn)
    return render(request, 'attendance/student_details.html', {'student': student})

def delete_student_view(request, usn):
    student = get_object_or_404(Student, usn=usn)
    if request.method == 'POST':
        student.delete()
        return redirect('view_students')  # Assuming 'view_students' is the name of the URL for the student list
    return render(request, 'attendance/delete_student.html', {'student': student})

from django.shortcuts import render, redirect
from .forms import StudentForm

def details_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_students')  # Redirect to the view_students page after adding the student
    else:
        form = StudentForm()
    return render(request, 'attendance/details.html', {'form': form})
