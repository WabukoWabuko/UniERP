from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.utils import ERPAuthentication
from education_erp.models import EducationUser, Student, Staff, Attendance, Fee, Course, Assignment, Grade
from small_business_erp.models import BusinessUser
from django.utils import timezone
from django.db.models import Sum
import logging

logger = logging.getLogger(__name__)

class DashboardView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        logger.info(f"Dashboard hub request user: {user.email}")

        available_erps = []
        if isinstance(user, EducationUser):
            available_erps.append({
                'id': 'education',
                'name': 'Education ERP',
                'url': '/dashboard/education/'
            })
        if isinstance(user, BusinessUser):
            available_erps.append({
                'id': 'small-business',
                'name': 'Small Business ERP',
                'url': '/dashboard/small-business/'
            })

        data = {'available_erps': available_erps}
        logger.info(f"Dashboard hub data: {data}")
        return Response(data)

class EducationDashboardView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        erp_id = request.auth['erp_id'] if request.auth else 'education'
        logger.info(f"Education dashboard request user: {user.email}, erp_id: {erp_id}")

        if not isinstance(user, EducationUser) or erp_id != 'education':
            logger.error(f"Invalid user or erp_id: {user}, {erp_id}")
            return Response({'error': 'Not an Education ERP user'}, status=403)

        if user.erp_role != 'admin' and not user.permissions.get('view_dashboard', False):
            logger.error(f"User {user.email} denied - no dashboard access")
            return Response({'error': 'Permission denied'}, status=403)

        students = Student.objects.filter(user=user).count()
        staff = Staff.objects.filter(user=user).count()
        fees_due = Fee.objects.filter(user=user, paid=False).aggregate(Sum('amount'))['amount__sum'] or 0
        attendance_today = Attendance.objects.filter(date=timezone.now().date(), present=True).count()
        data = {
            'total_students': students,
            'total_staff': staff,
            'total_fees_due': float(fees_due),
            'attendance_today': attendance_today,
        }
        logger.info(f"Education dashboard data: {data}")
        return Response(data)

class SchedulingView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        erp_id = request.auth['erp_id'] if request.auth else 'education'
        logger.info(f"Scheduling request user: {user.email}, erp_id: {erp_id}")

        if not isinstance(user, EducationUser) or erp_id != 'education':
            logger.error(f"Invalid user or erp_id: {user}, {erp_id}")
            return Response({'error': 'Not an Education ERP user'}, status=403)

        if not user.permissions.get('view_scheduling', False):
            logger.error(f"User {user.email} denied - no scheduling access")
            return Response({'error': 'Permission denied'}, status=403)

        fees = Fee.objects.filter(user=user).values('student__name', 'amount', 'due_date', 'paid')
        data = {'fees': list(fees)}
        logger.info(f"Scheduling data: {data}")
        if not data['fees']:
            return Response({'error': 'No fees found'}, status=404)
        return Response(data)

    def post(self, request):
        user = request.user
        if not user.permissions.get('edit_scheduling', False):
            return Response({'error': 'Permission denied'}, status=403)
        # Add fee logic here (simplified)
        data = request.data
        fee = Fee.objects.create(user=user, student=Student.objects.get(id=data['student_id']), amount=data['amount'], due_date=data['due_date'], paid=False)
        return Response({'id': fee.id, **data})

    def put(self, request, fee_id):
        user = request.user
        if not user.permissions.get('edit_scheduling', False):
            return Response({'error': 'Permission denied'}, status=403)
        fee = Fee.objects.get(id=fee_id, user=user)
        fee.paid = True
        fee.paid_date = timezone.now()
        fee.save()
        return Response({'status': 'updated'})

class StaffManagementView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        erp_id = request.auth['erp_id'] if request.auth else 'education'
        logger.info(f"Staff management request user: {user.email}, erp_id: {erp_id}")

        if not isinstance(user, EducationUser) or erp_id != 'education':
            logger.error(f"Invalid user or erp_id: {user}, {erp_id}")
            return Response({'error': 'Not an Education ERP user'}, status=403)

        if not user.permissions.get('view_staff', False):
            logger.error(f"User {user.email} denied - no staff access")
            return Response({'error': 'Permission denied'}, status=403)

        staff = Staff.objects.filter(user=user).values('name', 'staff_id', 'role', 'hire_date', 'salary', 'tax_rate', 'leave_balance')
        payroll = [
            {
                'name': s['name'],
                'staff_id': s['staff_id'],
                'role': s['role'],
                'hire_date': s['hire_date'],
                'gross': float(s['salary']),
                'tax_percent': float(s['tax_rate']),
                'net': float(s['salary']) * (1 - float(s['tax_rate']) / 100),
                'leave': s['leave_balance']
            } for s in staff
        ]
        data = {'payroll': payroll}
        logger.info(f"Staff management data: {data}")
        if not data['payroll']:
            return Response({'error': 'No staff found'}, status=404)
        return Response(data)

class LmsDashboardView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        erp_id = request.auth['erp_id'] if request.auth else 'education'
        logger.info(f"LMS dashboard request user: {user.email}, erp_id: {erp_id}")

        if not isinstance(user, EducationUser) or erp_id != 'education':
            logger.error(f"Invalid user or erp_id: {user}, {erp_id}")
            return Response({'error': 'Not an Education ERP user'}, status=403)

        if user.erp_role == 'student' and not user.permissions.get('view_courses', False):
            logger.error(f"Student {user.email} denied - no course access")
            return Response({'error': 'Permission denied'}, status=403)
        elif user.erp_role == 'teacher' and not user.permissions.get('manage_courses', False):
            logger.error(f"Teacher {user.email} denied - no course management access")
            return Response({'error': 'Permission denied'}, status=403)

        courses = Course.objects.filter(students__user=user) if user.erp_role == 'student' else Course.objects.filter(teacher__user=user)
        assignments = Assignment.objects.filter(course__in=courses)
        grades = Grade.objects.filter(student__user=user) if user.erp_role == 'student' else []
        data = {
            'courses': [{'id': c.id, 'name': c.name, 'code': c.code} for c in courses],
            'assignments': [{'id': a.id, 'title': a.title, 'due_date': a.due_date.isoformat()} for a in assignments],
            'grades': [{'assignment': g.assignment.title, 'score': g.score} for g in grades]
        }
        logger.info(f"LMS dashboard data: {data}")
        return Response(data)
