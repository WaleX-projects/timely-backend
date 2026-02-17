
# app/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField  # works well with Postgres
import json
from django.contrib.auth.models import User 
from django.db import models
from django.contrib.auth.models import User

class Classroom(models.Model):
    # Using a CharField for ID if you are generating custom strings in JS, 
    # otherwise, Django's default AutoField is usually better.

    
    name = models.CharField(max_length=255, help_text="Name of the class or course")
    room = models.CharField(max_length=50, blank=True, help_text="Room number or identifier")
    building = models.CharField(max_length=255, blank=True, help_text="Building or block name")
    
    # Coordinates and Radius
    latitude = models.FloatField(help_text="Classroom latitude")
    longitude = models.FloatField(help_text="Classroom longitude")
    radius_m = models.IntegerField(default=50, help_text="Allowed radius in meters")
    
    # Time fields (Ensure JS sends "HH:MM" or "HH:MM:SS" format)
    time_start = models.TimeField(help_text="Class start time")
    time_end = models.TimeField(help_text="Class end time")
    
    # Teacher: If JS sends a username or ID, your view logic will need to 
    # map that string to this ForeignKey.
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classrooms")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Classroom"
        verbose_name_plural = "Classrooms"

    def __str__(self):
        return f"{self.name} ({self.room})"
# app/models.py


class StudentFace(models.Model):
    name = models.CharField(max_length=255)
    matric_no = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ['matric_no']
    def __str__(self):
        return self.name


class StudentAttendance(models.Model):
    # Standard naming: 'student' (singular) for a ForeignKey
    student = models.ForeignKey(StudentFace, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    attendance_taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent a student from marking attendance twice in the SAME classroom 
        # on the SAME day (This requires a bit of extra logic in the view, 
        # but this unique constraint helps keep data clean)
        unique_together = ['student', 'classroom', 'attendance_taken_at']

    def __str__(self):
        return f"{self.student.name} in {self.classroom.name} at {self.attendance_taken_at}"


