from django.urls import path

from apps import views

urlpatterns = [
    path('index/',views.index),
    path('users/',views.UserView.as_view()),
    path('users/<str:pk>/',views.UserView.as_view()),
    path('students/',views.StudentView.as_view()),
    path('students<str:pk>/',views.StudentView.as_view()),
    path('employees/',views.EmployeeAPIView.as_view()),
    path('employees<str:pk>/',views.EmployeeAPIView.as_view()),

]