from django.contrib import admin
from .models import StudentFace,Classroom,StudentAttendance
# Register your models here.
admin.site.register(StudentAttendance)
admin.site.register(StudentFace)
admin.site.register(Classroom)