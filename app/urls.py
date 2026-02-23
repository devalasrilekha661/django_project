from django.urls import path
from .views import home, register, login, login_validation, teachersdashboard, studentsdashboard, add_student,edit_student,delete_student,logout_view

urlpatterns = [
  path('', register, name='register'),
    path("login/", login),
   path("login_validation/", login_validation, name="login_validation"),
   path("teachersdashboard/<int:id>/", teachersdashboard, name="teachersdashboard"),
path("students/<int:id>/edit/", edit_student, name="edit_student"),
    path("teachers/<int:id>/addstudent/", add_student, name="add_student"),
#    path("teachers/<int:id>/edit/", edit_student, name="edit_student"),
path("logout/", logout_view, name="logout"),
 path("delete_student/<int:id>/", delete_student, name="delete_student"),

    path("studentsdashboard/<int:id>/", studentsdashboard),
]
