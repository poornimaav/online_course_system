from django.contrib import admin
from .models import User, Course, Content, Purchase
# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Content)
admin.site.register(Purchase)