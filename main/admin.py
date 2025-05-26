from django.contrib import admin
from .models import Course,Student,Tutor,Enrollment,Profile,Location
# Register your models here.
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Enrollment)
admin.site.register(Profile)
admin.site.register(Location)