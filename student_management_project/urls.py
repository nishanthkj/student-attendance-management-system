from django.contrib import admin
from django.urls import path
from attendance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mark-attendance/', views.mark_attendance, name='mark-attendance'),
    path('login/', views.login_view, name='login'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('dash/', views.dash_view, name='dash'),
    path('add/', views.add_view, name='details'),
    path('view-students/', views.view_students, name='view-students'),
    path('', views.index_view, name='index'),
]
