# app/serializers.py
from rest_framework import serializers
from .models import Classroom,StudentFace,StudentAttendance

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            'id', 'name', 'room', 'building',
            'latitude', 'longitude', 'radius_m',
            'time_start', 'time_end', 'teacher'
        ]



class StudentFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFace
        fields = ['id', 'name', 'matric_no','face_encoding']



class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'