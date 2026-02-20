from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Student
import json

# --------------------------
# Home / Landing Page
# --------------------------
def home(request):
    return render(request, "registration.html")

def logout_view(request):
    request.session.flush()
    return redirect("/login/")

# --------------------------
# Teacher Views
# --------------------------
def teachersdashboard(request, id):
    teacher = User.objects.get(id=id)
    students = Student.objects.filter(teacher=teacher)

    return render(request, 'teachersdashboard.html', {
        'teacher': teacher,
        'students': students
    })


def add_student(request, id):
    teacher = get_object_or_404(User, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phNum = request.POST.get("phNum")
        course = request.POST.get("course")
        age = request.POST.get("age")

        # Create User first
        user = User.objects.create(
            name=name,
            email=email,
            phNum=phNum,
            password="123456",   # temporary default password
            role="Student"
        )

        # Then create Student profile
        Student.objects.create(
            user=user,
            teacher=teacher,
            course=course,
            age=age
        )

        return redirect("teachersdashboard", id=id)

    return render(request, "add_student.html", {"teacher": teacher})


def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.user.name = request.POST['name']
        student.user.email = request.POST['email']
        student.user.phNum = request.POST['phNum']
        student.course = request.POST['course']
        student.user.phNum = request.POST.get('phNum') 
        student.age = request.POST['age']

        student.user.save()
        student.save()

        return redirect('teachersdashboard', id=student.teacher.id)

    return render(request, 'edit_student.html', {"student": student})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    teacher_id = student.teacher.id
    student.delete()
    return redirect('teachersdashboard', id=teacher_id)


# --------------------------
# Student Views
# --------------------------
def studentsdashboard(request, id):

    if request.session.get("user_id") != id or request.session.get("role") != "Student":
        return redirect("/login/")

    student = get_object_or_404(Student, user_id=id)
    classmates = student.teacher.students.all()

    return render(request, "studentsdashboard.html", {
        "student": student,
        "students": classmates
    })

# --------------------------
# Authentication
# --------------------------
@api_view(["GET"])
def login(request):
    return render(request, "login.html")

@api_view(["POST"])
def login_validation(request):

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"msg": "Invalid JSON"}, status=400)

    email = data.get("e")
    password = data.get("p")
    role = data.get("r")

    if not email or not password or not role:
        return JsonResponse({"msg": "All fields required"}, status=400)

    user = User.objects.filter(email=email, role=role).first()

    if not user:
        return JsonResponse({"msg": "User not found"}, status=400)

    # ✅ FIXED PASSWORD CHECK
    if not check_password(password, user.password):
        return JsonResponse({"msg": "Invalid credentials"}, status=400)

    request.session["user_id"] = user.id
    request.session["role"] = role

    if role == "Teacher":
        return JsonResponse({
            "msg": "Login successful",
            "id": user.id,
            "r_url": "teachersdashboard"
        })

    elif role == "Student":
        student = Student.objects.filter(user=user).first()

        if not student:
            return JsonResponse({"msg": "Student profile not found"}, status=400)

        return JsonResponse({
            "msg": "Login successful",
            "id": user.id,
            "r_url": "studentsdashboard"
        })

def register(request):
    if request.method != "POST":
        return render(request, "register.html")

    try:
        data = json.loads(request.body)
        name = data.get("n")
        email = data.get("e")
        phNum = data.get("ph")
        password = data.get("p")
        confirm_password = data.get("cp")
        role = data.get("r")

        if password != confirm_password:
            return JsonResponse({"msg": "Password not matched"}, status=400)

        # ✅ HASH PASSWORD HERE
        hashed_password = make_password(password)

        # ✅ Create User
        user = User.objects.create(
            name=name,
            email=email,
            phNum=phNum,
            password=hashed_password,
            role=role
        )

        # ✅ If Student → create Student profile
        if role == "Student":

            teacher = User.objects.filter(role="Teacher").first()

            if not teacher:
                return JsonResponse({"msg": "No teacher available"}, status=400)

            Student.objects.create(
                user=user,
                teacher=teacher,
                course="Not Assigned",
                age=18
            )

        return JsonResponse({"msg": f"{role} registered successfully"})

    except IntegrityError:
        return JsonResponse({"msg": "Email already exists"}, status=400)

    except Exception as e:
        return JsonResponse({"msg": str(e)}, status=500)