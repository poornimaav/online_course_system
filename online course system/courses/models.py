from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    is_teacher = models.BooleanField('Is teacher', default=False)
    is_student = models.BooleanField('Is student', default=False)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username

    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # major = models.CharField(max_length=50, blank=True, default=None)
    # university = models.CharField(max_length=100, blank=True, default=None)
    # degree = models.CharField(max_length=30, blank=True, default=None)

    def __str__(self):
        return self.user.username

class Content(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='course_contents')
    title = models.CharField(max_length=100)
    text = models.TextField()
    video_url = models.URLField(blank=True)

    def __str__(self):
       return self.title


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.DurationField(default=timedelta(0))
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        limit_choices_to={'is_teacher': True}
    )
    contents = models.ManyToManyField(
        Content, # Add the on_delete argument here
        related_name='courses',
      # Set null=True to allow the field to be empty
        blank=True,
        null=True
    )
    purchased_by = models.ManyToManyField(User, related_name='purchased_courses',  blank=True,)


    def is_purchased_by_user(self, user):
        return self.purchased_by.filter(id=user.id).exists()

    def mark_as_purchased(self, user, transaction_id):
        self.purchased_by.add(user)
        purchase = Purchase(course=self, student=user, teacher=self.teacher, transaction_id=transaction_id)
        purchase.save()

    # def mark_as_purchased(self, user):
        # self.purchased_by.add(user)
        # purchase = Purchase(course=self, student=user)
        # purchase.save()

    def get_purchased_students(self):

        User = get_user_model()
        return User.objects.filter(purchased_courses=self, is_student=True)
        # def __str__(self):
        #     return self.User.title
        # return self.purchased_by.filter(is_student=True)

    def __str__(self):
        return self.title




class Purchase(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_purchases')
    purchased_at = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=100, default=0)

    def __str__(self):
        return f"{self.student.username} purchased {self.course.title} from {self.teacher.username} at {self.purchased_at}"

