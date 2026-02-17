# app/serializers.py
from rest_framework import serializers
from .models import Classroom,StudentFace,StudentAttendance
from django.contrib.auth.models import User

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            'id', 'name', 'room', 'building',
            'latitude', 'longitude', 'radius_m',
            'time_start', 'time_end', 'teacher'
        ]
        read_only_fields = ['teacher', 'id']



class StudentFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFace
        fields = ['id', 'name', 'matric_no','face_encoding']



class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_matric = serializers.CharField(source='student.matric_no', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    
    class Meta:
        model = StudentAttendance
        fields = ['id', 'student', 'classroom', 'student_name', 'student_matric', 'classroom_name', 'attendance_taken_at']
        read_only_fields = ['attendance_taken_at']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password')
    
    def create(self,validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')
    