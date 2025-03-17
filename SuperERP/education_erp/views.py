from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.utils import ERPAuthentication
from .models import EducationUser, Student, Staff
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

class StaffListView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        staff = Staff.objects.filter(user=request.user.user)
        data = [{
            'id': s.id,
            'name': s.name,
            'staff_id': s.staff_id,
            'role': s.role,
            'hire_date': s.hire_date,
            'salary': float(s.salary),  # Convert Decimal to float for JSON
        } for s in staff]
        return Response(data)

    def post(self, request):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        name = request.data.get('name')
        staff_id = request.data.get('staff_id')
        role = request.data.get('role')
        salary = request.data.get('salary', 0.00)
        if not all([name, staff_id, role]):
            return Response({'error': 'Name, staff_id, and role are required'}, status=400)
        if Staff.objects.filter(staff_id=staff_id).exists():
            return Response({'error': 'Staff ID already exists'}, status=400)
        staff = Staff(
            user=request.user.user,
            name=name,
            staff_id=staff_id,
            role=role,
            salary=salary
        )
        staff.save()
        return Response({'message': 'Staff added successfully', 'id': staff.id}, status=201)

class StaffDetailView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, staff_id):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        try:
            staff = Staff.objects.get(id=staff_id, user=request.user.user)
            data = {
                'id': staff.id,
                'name': staff.name,
                'staff_id': staff.staff_id,
                'role': staff.role,
                'hire_date': staff.hire_date,
                'salary': float(staff.salary),
            }
            return Response(data)
        except ObjectDoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)

    def put(self, request, staff_id):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        try:
            staff = Staff.objects.get(id=staff_id, user=request.user.user)
            staff.name = request.data.get('name', staff.name)
            staff.staff_id = request.data.get('staff_id', staff.staff_id)
            staff.role = request.data.get('role', staff.role)
            staff.salary = request.data.get('salary', staff.salary)
            staff.save()
            return Response({'message': 'Staff updated successfully'})
        except ObjectDoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)

    def delete(self, request, staff_id):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        try:
            staff = Staff.objects.get(id=staff_id, user=request.user.user)
            staff.delete()
            return Response({'message': 'Staff deleted successfully'})
        except ObjectDoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)

class PayrollOverviewView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not isinstance(request.user.user, EducationUser):
            return Response({'error': 'Not authorized for Education ERP'}, status=403)
        staff = Staff.objects.filter(user=request.user.user)
        total_salary = sum(float(s.salary) for s in staff)
        data = {
            'total_staff': staff.count(),
            'total_salary': total_salary,
        }
        return Response(data)
