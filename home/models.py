from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('tutor', 'Tutor'),
    )
    # Link to the built-in User table
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    mobile = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    education_level = models.CharField(max_length=50)
    course_preference = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default='student')
   

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    duration = models.CharField(max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    tutors = models.ManyToManyField(User, blank=True,related_name="teaching_courses")
    students=models.ManyToManyField(User,blank=True,related_name='setcourses')

    def __str__(self):
        return self.name


class Material(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class Aiprompt(models.Model):
#     tutor = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     title=models.CharField(max_length=200)
#     personality = models.CharField(max_length=100)
#     prompt_type = models.CharField(max_length=100)
#     custom_prompt = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.prompt_title

class TutorChat(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_msgs")
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tutor_msgs")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.username