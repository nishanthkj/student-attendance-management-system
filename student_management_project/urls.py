from django.contrib import admin
from django.urls import path
from attendance.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    path('attendance/', attendance_view, name='attendance'),
    path('dash/', dash_view, name='dash'),
    path('add/', add_view, name='add'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('view_students/', view_students, name='view_students'),
    path('student/<str:usn>/', student_details_view, name='student_details'),
    path('student/<str:usn>/delete/', delete_student_view, name='delete_student'),
    path('details/', details_view, name='details'),  # Ensure this line is added
]
