import os
import cv2
import numpy as np
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from insightface.app import FaceAnalysis

from .models import Classroom, StudentFace,StudentAttendance
from .serializers import ClassroomSerializer, StudentFaceSerializer
from .vectordb_client import add_face_to_db, search_face
from datetime import date 


# --- 1. ViewSets ---
class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

# --- 2. Model Initialization ---
model_path = os.path.join(settings.BASE_DIR, 'my_models')
face_app = FaceAnalysis(
    name='buffalo_sc', 
    root=model_path, 
    providers=['CPUExecutionProvider']
)
face_app.prepare(ctx_id=0, det_size=(160, 160))

# --- 3. Registration View ---
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def register_face(request):
    name = request.data.get('name')
    matric_no = request.data.get('matric_no')
    face_file = request.FILES.get('face_image')

    if not all([name, matric_no, face_file]):
        return Response({"status": "error", "message": "Missing name, matric_no, or face_image"}, status=400)


    # Decode image
    img_array = np.frombuffer(face_file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Generate embedding
    faces = face_app.get(img)
    if not faces:
        return Response({"status": "error", "message": "No face detected during registration"}, status=400)
    
    embedding = faces[0].normed_embedding.tolist()
    #Store user in normal Database
    student = StudentFace.objects.create(
        name=name,
        matric_no=matric_no
    )

    # Store in Vector DB
    response = add_face_to_db(matric_no, name, embedding)
    return Response(response)

# --- 4. Attendance View ---

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def get_faces(request):
    class_id = request.data.get('class_id')
    face_file = request.FILES.get('face_image')

    if not face_file or not class_id:
        return Response({"status": "error", "message": "Missing face image or classroom ID"}, status=400)

    # 1. Decode Image
    img_array = np.frombuffer(face_file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # 2. Extract Embedding
    faces = face_app.get(img)
    if not faces:
        return Response({"status": "error", "message": "No face found in frame"}, status=400)

    embedding = faces[0].normed_embedding.tolist()

    # 3. Search ChromaDB
    user_id, distance = search_face(embedding)

    if user_id and distance < 0.6:
        try:
            # 4. Fetch Student and Classroom Instances
            student = StudentFace.objects.get(matric_no=user_id)
            
            # CRITICAL FIX: Fetch the actual Classroom object
            try:
                classroom = Classroom.objects.get(id=class_id)
            except (Classroom.DoesNotExist, ValueError):
                return Response({"status": "error", "message": "Invalid Classroom ID"}, status=404)

            # 5. PREVENTION: Check if attendance was already marked TODAY
            already_marked = StudentAttendance.objects.filter(
                student=student,
                classroom=classroom,
                attendance_taken_at__date=date.today() # Only checks the date part
            ).exists()

            if already_marked:
                return Response({
                    "status": "warning", 
                    "message": f"Attendance already recorded for {student.name} today."
                }, status=200)

            # 6. Store Attendance
            StudentAttendance.objects.create(
                student=student,
                classroom=classroom  # Must be the object, not the ID
            )

            return Response({
                "status": "success", 
                "name": student.name,
                "matric_no": user_id,
                "confidence": round(1 - distance, 2)
            })

        except StudentFace.DoesNotExist:
            return Response({"status": "error", "message": "Student recognized by AI but missing in database"}, status=404)
    
    return Response({"status": "error", "message": "Identity not verified"}, status=401)