from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.utils import ERPAuthentication
from .models import EducationUser, Student, Staff, Attendance, Grade, Timetable, Fee
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Sum, Avg
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

class EducationDashboardView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser):
            return Response({'error': 'Not authorized'}, status=403)
        if user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
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
        return Response(data)

class StudentListView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser):
            return Response({'error': 'Not authorized'}, status=403)
        students = Student.objects.filter(user=user)
        data = [{
            'id': s.id, 'name': s.name, 'student_id': s.student_id, 'grade': s.grade,
            'enrollment_date': s.enrollment_date, 'date_of_birth': s.date_of_birth,
        } for s in students]
        return Response(data)

    def post(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        name = request.data.get('name')
        student_id = request.data.get('student_id')
        grade = request.data.get('grade')
        date_of_birth = request.data.get('date_of_birth')
        if not all([name, student_id, grade]):
            return Response({'error': 'Name, student_id, and grade required'}, status=400)
        if Student.objects.filter(student_id=student_id).exists():
            return Response({'error': 'Student ID exists'}, status=400)
        student = Student(user=user, name=name, student_id=student_id, grade=grade, date_of_birth=date_of_birth)
        student.save()
        return Response({'message': 'Student added', 'id': student.id}, status=201)

class StudentDetailView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        user = request.user.user
        if not isinstance(user, EducationUser):
            return Response({'error': 'Not authorized'}, status=403)
        try:
            student = Student.objects.get(id=student_id, user=user)
            data = {
                'id': student.id, 'name': student.name, 'student_id': student.student_id,
                'grade': student.grade, 'enrollment_date': student.enrollment_date,
                'date_of_birth': student.date_of_birth,
            }
            return Response(data)
        except ObjectDoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

    def put(self, request, student_id):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        try:
            student = Student.objects.get(id=student_id, user=user)
            student.name = request.data.get('name', student.name)
            student.student_id = request.data.get('student_id', student.student_id)
            student.grade = request.data.get('grade', student.grade)
            student.date_of_birth = request.data.get('date_of_birth', student.date_of_birth)
            student.save()
            return Response({'message': 'Student updated'})
        except ObjectDoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

    def delete(self, request, student_id):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        try:
            student = Student.objects.get(id=student_id, user=user)
            student.delete()
            return Response({'message': 'Student deleted'})
        except ObjectDoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class AttendanceView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser):
            return Response({'error': 'Not authorized'}, status=403)
        date = request.query_params.get('date', timezone.now().date())
        attendance = Attendance.objects.filter(student__user=user, date=date)
        data = [{'student_id': a.student.id, 'name': a.student.name, 'present': a.present} for a in attendance]
        return Response(data)

    def post(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role not in ['admin', 'teacher']:
            return Response({'error': 'Admin/Teacher access only'}, status=403)
        student_id = request.data.get('student_id')
        present = request.data.get('present', False)
        date = request.data.get('date', timezone.now().date())
        try:
            student = Student.objects.get(id=student_id, user=user)
            attendance, created = Attendance.objects.get_or_create(student=student, date=date, defaults={'present': present})
            if not created:
                attendance.present = present
                attendance.save()
            return Response({'message': 'Attendance updated'})
        except ObjectDoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class GradeView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser):
            return Response({'error': 'Not authorized'}, status=403)
        student_id = request.query_params.get('student_id')
        if student_id:
            grades = Grade.objects.filter(student__id=student_id, student__user=user)
        else:
            grades = Grade.objects.filter(student__user=user)
        data = [{'student_id': g.student.id, 'subject': g.subject, 'grade': float(g.grade_value), 'date': g.date_recorded} for g in grades]
        return Response(data)

    def post(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role not in ['admin', 'teacher']:
            return Response({'error': 'Admin/Teacher access only'}, status=403)
        student_id = request.data.get('student_id')
        subject = request.data.get('subject')
        grade_value = request.data.get('grade_value')
        if not all([student_id, subject, grade_value]):
            return Response({'error': 'All fields required'}, status=400)
        try:
            student = Student.objects.get(id=student_id, user=user)
            grade = Grade(student=student, subject=subject, grade_value=grade_value)
            grade.save()
            return Response({'message': 'Grade added'})
        except ObjectDoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class StaffListView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser):
            return Response({'error': 'Not authorized'}, status=403)
        staff = Staff.objects.filter(user=user)
        data = [{
            'id': s.id, 'name': s.name, 'staff_id': s.staff_id, 'role': s.role,
            'hire_date': s.hire_date, 'salary': float(s.salary), 'tax_rate': float(s.tax_rate),
            'leave_balance': s.leave_balance,
        } for s in staff]
        return Response(data)

    def post(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        name = request.data.get('name')
        staff_id = request.data.get('staff_id')
        role = request.data.get('role')
        salary = request.data.get('salary', 0.00)
        tax_rate = request.data.get('tax_rate', 10.00)
        if not all([name, staff_id, role]):
            return Response({'error': 'Name, staff_id, and role required'}, status=400)
        if Staff.objects.filter(staff_id=staff_id).exists():
            return Response({'error': 'Staff ID exists'}, status=400)
        staff = Staff(user=user, name=name, staff_id=staff_id, role=role, salary=salary, tax_rate=tax_rate)
        staff.save()
        return Response({'message': 'Staff added', 'id': staff.id}, status=201)

class StaffDetailView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, staff_id):
        user = request.user.user
        if not isinstance(user, EducationUser):
            return Response({'error': 'Not authorized'}, status=403)
        try:
            staff = Staff.objects.get(id=staff_id, user=user)
            data = {
                'id': staff.id, 'name': staff.name, 'staff_id': staff.staff_id,
                'role': staff.role, 'hire_date': staff.hire_date, 'salary': float(staff.salary),
                'tax_rate': float(staff.tax_rate), 'leave_balance': staff.leave_balance,
            }
            return Response(data)
        except ObjectDoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)

    def put(self, request, staff_id):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        try:
            staff = Staff.objects.get(id=staff_id, user=user)
            staff.name = request.data.get('name', staff.name)
            staff.staff_id = request.data.get('staff_id', staff.staff_id)
            staff.role = request.data.get('role', staff.role)
            staff.salary = request.data.get('salary', staff.salary)
            staff.tax_rate = request.data.get('tax_rate', staff.tax_rate)
            staff.leave_balance = request.data.get('leave_balance', staff.leave_balance)
            staff.save()
            return Response({'message': 'Staff updated'})
        except ObjectDoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)

    def delete(self, request, staff_id):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        try:
            staff = Staff.objects.get(id=staff_id, user=user)
            staff.delete()
            return Response({'message': 'Staff deleted'})
        except ObjectDoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)

class PayrollOverviewView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        staff = Staff.objects.filter(user=user)
        data = []
        for s in staff:
            net_salary = float(s.salary) * (1 - float(s.tax_rate) / 100)
            data.append({
                'name': s.name, 'staff_id': s.staff_id, 'gross_salary': float(s.salary),
                'tax_rate': float(s.tax_rate), 'net_salary': net_salary, 'leave_balance': s.leave_balance,
            })
        total_net = sum(d['net_salary'] for d in data)
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = [Paragraph("Payroll Report", getSampleStyleSheet()['Heading1'])]
        table_data = [['Name', 'Staff ID', 'Gross Salary', 'Tax Rate', 'Net Salary', 'Leave Balance']] + \
                     [[d['name'], d['staff_id'], f"${d['gross_salary']:.2f}", f"{d['tax_rate']}%", f"${d['net_salary']:.2f}", d['leave_balance']] for d in data]
        table = Table(table_data, colWidths=[100, 80, 80, 60, 80, 80])
        table.setStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return Response({'payroll': data, 'total_net_salary': total_net, 'report_pdf': buffer.getvalue().hex()})

class TimetableListView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser):
            return Response({'error': 'Not authorized'}, status=403)
        timetable = Timetable.objects.filter(user=user)
        data = [{
            'id': t.id, 'staff_name': t.staff.name, 'student_name': t.student.name,
            'subject': t.subject, 'day_of_week': t.day_of_week,
            'start_time': t.start_time.strftime('%H:%M'), 'end_time': t.end_time.strftime('%H:%M'),
        } for t in timetable]
        return Response(data)

    def post(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        staff_id = request.data.get('staff_id')
        student_id = request.data.get('student_id')
        subject = request.data.get('subject')
        day_of_week = request.data.get('day_of_week')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        if not all([staff_id, student_id, subject, day_of_week, start_time, end_time]):
            return Response({'error': 'All fields required'}, status=400)
        try:
            staff = Staff.objects.get(id=staff_id, user=user)
            student = Student.objects.get(id=student_id, user=user)
            conflicts = Timetable.objects.filter(
                user=user, day_of_week=day_of_week
            ).filter(
                models.Q(staff=staff) | models.Q(student=student)
            ).filter(
                models.Q(start_time__lte=start_time, end_time__gte=start_time) |
                models.Q(start_time__lte=end_time, end_time__gte=end_time) |
                models.Q(start_time__gte=start_time, end_time__lte=end_time)
            )
            if conflicts.exists():
                return Response({'error': 'Schedule conflict detected'}, status=400)
            timetable = Timetable(
                user=user, staff=staff, student=student, subject=subject,
                day_of_week=day_of_week, start_time=start_time, end_time=end_time
            )
            timetable.save()
            return Response({'message': 'Timetable entry added', 'id': timetable.id}, status=201)
        except ObjectDoesNotExist:
            return Response({'error': 'Staff or Student not found'}, status=404)

class FeeListView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser):
            return Response({'error': 'Not authorized'}, status=403)
        fees = Fee.objects.filter(user=user)
        data = [{
            'id': f.id, 'student_name': f.student.name, 'amount': float(f.amount),
            'due_date': f.due_date, 'paid': f.paid, 'paid_date': f.paid_date,
            'overdue': f.due_date < timezone.now().date() and not f.paid,
        } for f in fees]
        total_due = sum(float(f.amount) for f in fees.filter(paid=False))
        total_paid = sum(float(f.amount) for f in fees.filter(paid=True))
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = [Paragraph("Fee Report", getSampleStyleSheet()['Heading1'])]
        table_data = [['Student', 'Amount', 'Due Date', 'Paid', 'Paid Date']] + \
                     [[f['student_name'], f"${f['amount']:.2f}", f['due_date'], 'Yes' if f['paid'] else 'No', f['paid_date'] or 'N/A'] for f in data]
        table = Table(table_data, colWidths=[120, 80, 80, 60, 80])
        table.setStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return Response({'fees': data, 'total_due': total_due, 'total_paid': total_paid, 'report_pdf': buffer.getvalue().hex()})

    def post(self, request):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        student_id = request.data.get('student_id')
        amount = request.data.get('amount')
        due_date = request.data.get('due_date')
        if not all([student_id, amount, due_date]):
            return Response({'error': 'All fields required'}, status=400)
        try:
            student = Student.objects.get(id=student_id, user=user)
            fee = Fee(user=user, student=student, amount=amount, due_date=due_date)
            fee.save()
            return Response({'message': 'Fee added', 'id': fee.id}, status=201)
        except ObjectDoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

class FeeDetailView(APIView):
    authentication_classes = [ERPAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, fee_id):
        user = request.user.user
        if not isinstance(user, EducationUser) or user.erp_role != 'admin':
            return Response({'error': 'Admin access only'}, status=403)
        try:
            fee = Fee.objects.get(id=fee_id, user=user)
            paid = request.data.get('paid', fee.paid)
            if paid and not fee.paid:
                fee.paid = True
                fee.paid_date = timezone.now().date()
            fee.save()
            return Response({'message': 'Fee updated'})
        except ObjectDoesNotExist:
            return Response({'error': 'Fee not found'}, status=404)
