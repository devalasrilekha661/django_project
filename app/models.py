from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phNum = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.email


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="students",
        limit_choices_to={'role': 'Teacher'}
    )
    course = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.user.name