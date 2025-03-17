from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.utils import ERPAuthentication
from .models import EducationUser, Student
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class EducationDashboardView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        return Response({'message': 'Welcome to Education ERP Dashboard!'})

class StudentListView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        students = Student.objects.filter(user=request.user.user)
        data = [{
            'id': student.id,
            'name': student.name,
            'student_id': student.student_id,
            'grade': student.grade,
            'enrollment_date': student.enrollment_date,
            'date_of_birth': student.date_of_birth,
        } for student in students]
        return Response(data)

    def post(self, request):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        name = request.data.get('name')
        student_id = request.data.get('student_id')
        grade = request.data.get('grade')
        date_of_birth = request.data.get('date_of_birth')
        if not all([name, student_id, grade]):
            return Response({'error': 'Name, student_id, and grade are required'}, status=400)
        if Student.objects.filter(student_id=student_id).exists():
            return Response({'error': 'Student ID already exists'}, status=400)
        student = Student(
            user=request.user.user,
            name=name,
            student_id=student_id,
            grade=grade,
            date_of_birth=date_of_birth
        )
        student.save()
        return Response({'message': 'Student added successfully', 'id': student.id}, status=201)

class StudentDetailView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        try:
            student = Student.objects.get(id=student_id, user=request.user.user)
            data = {
                'id': student.id,
                'name': student.name,
                'student_id': student.student_id,
                'grade': student.grade,
                'enrollment_date': student.enrollment_date,
                'date_of_birth': student.date_of_birth,
            }
            return Response(data)
        except ObjectDoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

    def put(self, request, student_id):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        try:
            student = Student.objects.get(id=student_id, user=request.user.user)
            student.name = request.data.get('name', student.name)
            student.student_id = request.data.get('student_id', student.student_id)
            student.grade = request.data.get('grade', student.grade)
            student.date_of_birth = request.data.get('date_of_birth', student.date_of_birth)
            student.save()
            return Response({'message': 'Student updated successfully'})
        except ObjectDoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

    def delete(self, request, student_id):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        try:
            student = Student.objects.get(id=student_id, user=request.user.user)
            student.delete()
            return Response({'message': 'Student deleted successfully'})
        except ObjectDoesNotExist:
            return Response({'error': 'Student not found'}, status=404)
