from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20, unique=True)
    face_embedding = models.BinaryField()
    

    def __str__(self):
        return f'{self.name} ({self.usn})({self.face_embedding})'

class Log(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.name} - {self.timestamp}'
