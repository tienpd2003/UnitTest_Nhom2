import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
from course.models import *
from login_std.models import profile_std
from faculty.models import Department, FacultyClasses, idCourse, Faculty
from tuitionfee.models import tuitionfee_scale as TuitionFeeScale
from schedule.models import ScheduleModuleClass
from tuitionfee.models import tuitionfee
import json

# Fixtures for test data
@pytest.fixture
def faculty():
    return Faculty.objects.create(
        idFaculty='FAC1',
        nameFaculty='Test Faculty'
    )

@pytest.fixture
def department(faculty):
    return Department.objects.create(
        idDepartment='DEP1',
        nameDepartment='Test Department',
        faculty=faculty
    )

@pytest.fixture
def course():
    return idCourse.objects.create(
        idCourse='K1',
        nameCourse='Test Course'
    )

@pytest.fixture
def faculty_class(course, department):
    return FacultyClasses.objects.create(
        idClass='CLS1',
        idCourse=course,
        department=department
    )

@pytest.fixture
def semester():
    return Semester.objects.create(
        idSemester='SEM1',
        nameSemester='Test Semester',
        start_date=timezone.now().date(),
        end_date=(timezone.now() + timedelta(days=120)).date()
    )

@pytest.fixture
def tuitionfee_scale(semester):
    return TuitionFeeScale.objects.create(
        idSemester=semester,
        scale=Decimal('850000.00')  # 850,000 VND per credit
    )

@pytest.fixture
def module(department):
    return Module.objects.create(
        idModule='MOD1',
        nameModule='Test Module',
        credits=3,
        department=department,
        final_ratio=0.6,
        process_ratio=0.4
    )

@pytest.fixture
def module_class(module, faculty_class, semester):
    return ModuleClass.objects.create(
        module=module,
        idClass=faculty_class,
        semester=semester,
        max_slot=40
    )

@pytest.fixture
def student(faculty_class):
    return profile_std.objects.create(
        idStd='STD1',
        password='testpass123',
        nameStd='Test Student',
        datebirthStd=date(2000, 1, 1),
        genderStd='Nam',
        ethnicityStd='Kinh',
        addressStd='Test Address',
        idClass=faculty_class,
        graduate=True,
        is_active=True
    )

@pytest.fixture
def registration(semester, course):
    return RegistrationSchedule.objects.create(
        semester=semester,
        idCourse=course,
        start_date=timezone.now().date(),
        end_date=(timezone.now() + timedelta(days=30)).date()
    )

@pytest.fixture
def client_with_auth(client, student):
    client.force_login(student, backend='login_std.backends.CustomAuthBackendStd')
    session = client.session
    session['_auth_user_id'] = student.idStd
    session['_auth_user_backend'] = 'login_std.backends.CustomAuthBackendStd'
    session.save()
    return client

# Test cases
@pytest.mark.django_db
class TestModuleClass:
    def test_create_moduleclass(self, module_class):
        assert module_class.pk is not None
        assert module_class.max_slot == 40
        assert isinstance(module_class.module, Module)
        assert isinstance(module_class.idClass, FacultyClasses)
        assert isinstance(module_class.semester, Semester)

    def test_create_student_moduleclass(self, module_class, student, tuitionfee_scale):
        # Tạo học phí trước
        tuition = tuitionfee.objects.create(
            idStd=student,
            idSemester=module_class.semester,
            totalcredit=module_class.module.credits,
            total_tuitionfee=str(int(module_class.module.credits * tuitionfee_scale.scale))
        )

        student_module = Student_ModuleClass.objects.create(
            module_class=module_class,
            idStd=student
        )
        assert student_module.pk is not None
        assert student_module.module_class == module_class
        assert student_module.idStd == student
        
        # Kiểm tra học phí được tính
        expected_fee = str(int(module_class.module.credits * tuitionfee_scale.scale))
        tuition = tuitionfee.objects.filter(
            idStd=student,
            idSemester=module_class.semester
        ).first()
        assert tuition is not None
        assert tuition.total_tuitionfee == expected_fee

@pytest.mark.django_db
class TestModuleRegistrationView:
    def test_module_registration_view_in_time(self, client_with_auth, registration):
        response = client_with_auth.get(reverse('module_registration'))
        assert response.status_code == 200
        assert 'module_registration.html' in [t.name for t in response.templates]

    def test_get_moduleclass(self, client_with_auth, module_class, student, semester):
        from course.views import global_semester
        global global_semester
        global_semester = semester.idSemester
        
        response = client_with_auth.get(
            reverse('get_moduleclass_std', kwargs={'idStd': student.idStd})
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data['moduleclasses']) == 1

    def test_save_moduleclass_success(self, client_with_auth, module_class, student, semester, tuitionfee_scale):
        from course.views import global_semester
        global global_semester
        global_semester = semester.idSemester
        
        response = client_with_auth.post(
            reverse('save_moduleclass_std', kwargs={'idStd': student.idStd}),
            data=json.dumps([module_class.idModuleClass]),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['success'] is True
        
        # Check DB
        saved = Student_ModuleClass.objects.filter(
            idStd=student,
            module_class=module_class
        ).exists()
        assert saved is True

        # Check tuition fee
        expected_fee = str(int(module_class.module.credits * tuitionfee_scale.scale))
        tuition = tuitionfee.objects.filter(
            idStd=student,
            idSemester=semester
        ).first()
        assert tuition is not None
        assert tuition.total_tuitionfee == expected_fee

    def test_search_moduleclass(self, client_with_auth, module_class, semester):
        from course.views import global_semester
        global global_semester
        global_semester = semester.idSemester

        # Test tìm theo mã học phần
        response = client_with_auth.get(
            reverse('search_moduleclass_std', kwargs={'value': 'MOD1'})
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data['moduleclasses']) == 1

        # Test tìm theo tên học phần
        response = client_with_auth.get(
            reverse('search_moduleclass_std', kwargs={'value': 'Test Module'})
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data['moduleclasses']) == 1

        # Test không tìm thấy
        response = client_with_auth.get(
            reverse('search_moduleclass_std', kwargs={'value': 'NOT_EXIST'})
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data['moduleclasses']) == 0

    def test_get_detail_schedule(self, client_with_auth, module_class):
        # Tạo lịch học
        schedule = ScheduleModuleClass.objects.create(
            idModuleClass=module_class,
            days_of_week=2,  # Thứ 2
            period_start=1
        )
        
        response = client_with_auth.get(
            reverse('get_detail_schedule_std', kwargs={'idModuleClass': module_class.idModuleClass})
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data['schedule']) == 1
        assert int(data['schedule'][0]['days_of_week']) == 2
        assert int(data['schedule'][0]['period_start']) == 1

    def test_get_saved_moduleclass(self, client_with_auth, student, module_class, semester, tuitionfee_scale):
        from course.views import global_semester
        global global_semester
        global_semester = semester.idSemester

        # Tạo đăng ký học phần
        Student_ModuleClass.objects.create(
            module_class=module_class,
            idStd=student
        )
        
        response = client_with_auth.get(
            reverse('get_saved_moduleclass_std', kwargs={'idStd': student.idStd})
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data['moduleclasses']) == 1
        assert data['moduleclasses'][0]['idModule'] == module_class.module.idModule

    def test_delete_moduleclass(self, client_with_auth, student, module_class, semester, tuitionfee_scale):
        # Tạo đăng ký học phần
        Student_ModuleClass.objects.create(
            module_class=module_class,
            idStd=student
        )
        
        response = client_with_auth.post(
            reverse('delete_moduleclass_std', kwargs={'idStd': student.idStd}),
            data=json.dumps([module_class.idModuleClass]),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['success'] is True
        
        # Kiểm tra xóa thành công
        assert not Student_ModuleClass.objects.filter(
            idStd=student,
            module_class=module_class
        ).exists()

    def test_check_duplicate_schedule(self, module_class, student, semester, tuitionfee_scale):
        # Tạo học phí trước
        total_fee = str(int(module_class.module.credits * tuitionfee_scale.scale))
        tuition = tuitionfee.objects.create(
            idStd=student,
            idSemester=semester,
            totalcredit=module_class.module.credits,
            total_tuitionfee=total_fee,
            paid_tuitionfee='0',
            unpaid_tuitionfee=total_fee
        )

        # Tạo 2 lịch học trùng nhau
        schedule1 = ScheduleModuleClass.objects.create(
            idModuleClass=module_class,
            days_of_week=2,  # Thứ 2
            period_start=1
        )
        
        module_class2 = ModuleClass.objects.create(
            module=module_class.module,
            idClass=module_class.idClass,
            semester=module_class.semester,
            max_slot=40
        )
        
        schedule2 = ScheduleModuleClass.objects.create(
            idModuleClass=module_class2,
            days_of_week=2,  # Thứ 2
            period_start=1
        )
        
        # Đăng ký học phần đầu tiên
        Student_ModuleClass.objects.create(
            module_class=module_class,
            idStd=student
        )
        
        # Kiểm tra trùng lịch khi đăng ký học phần thứ 2
        from course.views import check_duplicate_schedule
        assert check_duplicate_schedule(student, module_class2) is True 