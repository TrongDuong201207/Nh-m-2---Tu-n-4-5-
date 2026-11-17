from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from students.models import Student
from academics.models import Course, CourseSection
from enrollments.models import Enrollment
from .models import GradeComponent, Grade
from .services import calculate_final_grade

class GradeCalculationTests(TestCase):
    def setUp(self):
        student = Student.objects.create(student_code='25070011', full_name='Nguyễn Minh Anh', administrative_class='CNTT-K68', email='a@example.local')
        course = Course.objects.create(course_code='CS101', course_name='Nhập môn lập trình', credits=3)
        section = CourseSection.objects.create(course=course, section_code='CS101-01', semester='1', academic_year='2026-2027', status=CourseSection.Status.OPEN)
        self.enrollment = Enrollment.objects.create(student=student, course_section=section)
        self.assignment = GradeComponent.objects.create(course_section=section, component_name='Bài tập', weight_percent=Decimal('20.00'))
        self.midterm = GradeComponent.objects.create(course_section=section, component_name='Giữa kỳ', weight_percent=Decimal('30.00'))
        self.final = GradeComponent.objects.create(course_section=section, component_name='Cuối kỳ', weight_percent=Decimal('50.00'))

    def test_calculate_weighted_final_grade(self):
        Grade.objects.create(enrollment=self.enrollment, component=self.assignment, score=Decimal('8.00'))
        Grade.objects.create(enrollment=self.enrollment, component=self.midterm, score=Decimal('7.00'))
        Grade.objects.create(enrollment=self.enrollment, component=self.final, score=Decimal('9.00'))
        self.assertEqual(calculate_final_grade(self.enrollment), Decimal('8.20'))

    def test_reject_incomplete_weights(self):
        self.final.weight_percent = Decimal('40.00')
        self.final.save()
        with self.assertRaises(ValidationError):
            calculate_final_grade(self.enrollment)
