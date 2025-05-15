import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from decimal import Decimal, InvalidOperation
from login_std.models import profile_std
from faculty.models import FacultyClasses, idCourse, Faculty, Department
from course.models import *
from .models import *
from .views import *
import json
from datetime import date

"""
Module: Kiểm thử Module Học phí
Mô tả: Các test case cho chức năng quản lý học phí
Tác giả: [Tên của bạn]
Ngày tạo: [Ngày tạo]

Các test case được implement:
TC01: Kiểm tra tạo học phí cho sinh viên
TC02: Kiểm tra cập nhật học phí khi thêm học phần
TC03: Kiểm tra tính toán học phí chưa đóng
TC04: Kiểm tra xem học phí theo kỳ
TC05: Kiểm tra thanh toán học phí
TC06: Kiểm tra ràng buộc không trùng lặp học phí
TC07: Kiểm tra validation số tiền âm
TC08: Kiểm tra validation số tín chỉ âm
TC09: Kiểm tra độ chính xác của phép tính với số thập phân
TC10: Kiểm tra lấy danh sách học kỳ của sinh viên
TC11: Kiểm tra lấy danh sách học kỳ khi sinh viên chưa đăng ký học phần
TC12: Kiểm tra lấy danh sách học kỳ khi sinh viên đăng ký nhiều học kỳ
"""

# ---------- Fixtures ----------
@pytest.fixture
def client():
    return Client()

@pytest.fixture
def test_password():
    return 'test_password'

@pytest.fixture
def create_user(test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = 'testuser'
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def create_faculty():
    faculty = Faculty.objects.create(
        idFaculty="CNTT",
        nameFaculty="Công nghệ thông tin"
    )
    return faculty

@pytest.fixture
def create_department(create_faculty):
    department = Department.objects.create(
        idDepartment="KTPM",
        nameDepartment="Kỹ thuật phần mềm",
        faculty=create_faculty
    )
    return department

@pytest.fixture
def create_course():
    course = idCourse.objects.create(
        idCourse="K21",
        nameCourse="Khóa 2021"
    )
    return course

@pytest.fixture
def create_faculty_class(create_course, create_department):
    faculty_class = FacultyClasses.objects.create(
        idClass="KTPM2021",
        idCourse=create_course,
        department=create_department
    )
    return faculty_class

@pytest.fixture
def create_student(create_faculty_class):
    student = profile_std.objects.create(
        idStd="20110001",
        password="test_password",
        nameStd="Test Student",
        datebirthStd=date(2002, 1, 1),
        genderStd="Nam",
        ethnicityStd="Kinh",
        addressStd="Test Address",
        idClass=create_faculty_class,
        graduate=True,
        is_active=True
    )
    return student

@pytest.fixture
def create_semester():
    semester = Semester.objects.create(
        idSemester="HK1-23-24",
        nameSemester="Học kỳ 1 năm 2023-2024",
        start_date=date(2023, 9, 1),
        end_date=date(2024, 1, 31)
    )
    return semester

@pytest.fixture
def create_tuitionfee_scale(create_semester):
    scale = tuitionfee_scale.objects.create(
        idSemester=create_semester,
        scale=850000.0  # 850,000 VND per credit
    )
    return scale

@pytest.fixture
def create_module(create_department):
    module = Module.objects.create(
        idModule="CS101",
        nameModule="Introduction to Programming",
        credits=3,
        department=create_department,
        final_ratio=0.6,
        process_ratio=0.4
    )
    return module

@pytest.fixture
def create_moduleclass(create_module, create_faculty_class, create_semester):
    moduleclass = ModuleClass.objects.create(
        module=create_module,
        idClass=create_faculty_class,
        semester=create_semester,
        max_slot=40
    )
    return moduleclass

# ---------- Test Cases ----------
@pytest.mark.django_db
class TestTuitionFee:
    """
    Bộ test cho module học phí
    """

    def test_create_tuition_fee(self, client, create_student, create_semester, create_tuitionfee_scale):
        """
        TC01: Kiểm tra tạo học phí cho sinh viên
        - Đầu vào: Thông tin sinh viên và học kỳ
        - Xử lý: Tạo bản ghi học phí mới
        - Đầu ra mong đợi: Bản ghi học phí được tạo với các giá trị khởi tạo đúng
        """
        # Xóa các bản ghi học phí hiện có
        tuitionfee.objects.filter(idStd=create_student).delete()

        # Create tuition fee record
        tuition = tuitionfee.objects.create(
            idStd=create_student,
            idSemester=create_semester,
            totalcredit=0,
            total_tuitionfee="0",
            paid_tuitionfee="0",
            unpaid_tuitionfee="0"
        )

        # Verify tuition fee record
        assert tuition.idStd == create_student
        assert tuition.idSemester == create_semester
        assert tuition.totalcredit == 0
        assert tuition.total_tuitionfee == "0"
        assert tuition.paid_tuitionfee == "0"
        assert tuition.unpaid_tuitionfee == "0"

    def test_update_tuition_fee_on_moduleclass_add(self, client, create_student, create_semester, 
                                                 create_tuitionfee_scale, create_moduleclass):
        """
        TC02: Kiểm tra cập nhật học phí khi thêm học phần
        - Đầu vào: Sinh viên đăng ký học phần
        - Xử lý: Tạo quan hệ sinh viên-học phần và kiểm tra cập nhật học phí
        - Đầu ra mong đợi: Học phí được tính toán lại dựa trên số tín chỉ
        """
        # Xóa các bản ghi học phí hiện có
        tuitionfee.objects.filter(idStd=create_student).delete()

        # Create initial tuition fee
        initial_tuition = tuitionfee.objects.create(
            idStd=create_student,
            idSemester=create_semester,
            totalcredit=0,
            total_tuitionfee="0",
            paid_tuitionfee="0",
            unpaid_tuitionfee="0"
        )

        # Register student for module class
        student_moduleclass = Student_ModuleClass.objects.create(
            idStd=create_student,
            module_class=create_moduleclass
        )

        # Refresh tuition fee from database
        updated_tuition = tuitionfee.objects.get(idStd=create_student, idSemester=create_semester)
        
        # Verify updates
        assert updated_tuition.totalcredit == create_moduleclass.module.credits
        expected_fee = str(int(create_moduleclass.module.credits * create_tuitionfee_scale.scale))
        assert updated_tuition.total_tuitionfee == expected_fee
        assert updated_tuition.unpaid_tuitionfee == expected_fee

    def test_calculate_unpaid_tuition(self, client, create_student, create_semester, create_tuitionfee_scale):
        """
        TC03: Kiểm tra tính toán học phí chưa đóng
        - Đầu vào: Sinh viên có bản ghi học phí
        - Xử lý: Cập nhật số tiền đã đóng và kiểm tra tính toán số tiền chưa đóng
        - Đầu ra mong đợi: Số tiền chưa đóng được tính toán chính xác
        """
        # Xóa các bản ghi học phí hiện có
        tuitionfee.objects.filter(idStd=create_student).delete()

        # Create tuition fee record
        tuition = tuitionfee.objects.create(
            idStd=create_student,
            idSemester=create_semester,
            totalcredit=3,
            total_tuitionfee="2550000",  # 3 credits * 850,000
            paid_tuitionfee="1000000",
            unpaid_tuitionfee="1550000"
        )

        # Verify initial unpaid amount
        assert tuition.unpaid_tuitionfee == "1550000"

        # Update paid amount and recalculate unpaid amount
        tuition.paid_tuitionfee = "2000000"
        tuition.unpaid_tuitionfee = str(int(tuition.total_tuitionfee) - int(tuition.paid_tuitionfee))
        tuition.save()

        # Refresh from database
        tuition.refresh_from_db()

        # Verify updated unpaid amount
        assert tuition.unpaid_tuitionfee == "550000"

    def test_view_semester_tuition(self, client, create_student, create_semester, 
                                 create_tuitionfee_scale, create_moduleclass):
        """
        TC04: Kiểm tra xem học phí theo kỳ
        - Đầu vào: Thông tin sinh viên và học kỳ
        - Xử lý: Lấy thông tin học phí cho học kỳ
        - Đầu ra mong đợi: Trả về dữ liệu học phí chính xác
        """
        # Xóa các bản ghi học phí hiện có
        tuitionfee.objects.filter(idStd=create_student).delete()

        # Register student for module class first
        student_moduleclass = Student_ModuleClass.objects.create(
            idStd=create_student,
            module_class=create_moduleclass
        )

        # Login student
        client.force_login(create_student)

        # Make request
        response = client.get(reverse('get_tuitionfee'))
        
        # Verify response
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data['semester_tuitionfees']) == 1
        semester_data = data['semester_tuitionfees'][0]
        assert semester_data['semester'] == create_semester.nameSemester
        assert float(semester_data['tuitionfee']['total_tuitionfee']) == 2550000
        
        # Verify module class data
        assert len(semester_data['moduleclasses']) == 1
        moduleclass_data = semester_data['moduleclasses'][0]
        assert moduleclass_data['idModule'] == create_moduleclass.module.idModule
        assert moduleclass_data['nameModule'] == create_moduleclass.module.nameModule
        assert moduleclass_data['credit'] == create_moduleclass.module.credits
        assert moduleclass_data['idClass'] == create_moduleclass.idClass.idClass

    def test_payment_processing(self, client, create_student, create_semester, create_tuitionfee_scale):
        """
        TC05: Kiểm tra xử lý thanh toán
        - Đầu vào: Sinh viên có bản ghi học phí
        - Xử lý: Xử lý thanh toán và kiểm tra cập nhật
        - Đầu ra mong đợi: Số tiền đã đóng và chưa đóng được cập nhật chính xác
        """
        # Xóa các bản ghi học phí hiện có
        tuitionfee.objects.filter(idStd=create_student).delete()

        # Create tuition fee record
        tuition = tuitionfee.objects.create(
            idStd=create_student,
            idSemester=create_semester,
            totalcredit=3,
            total_tuitionfee="2550000",  # 3 credits * 850,000
            paid_tuitionfee="0",
            unpaid_tuitionfee="2550000"
        )

        # Process payment and recalculate unpaid amount
        payment_amount = "1500000"
        tuition.paid_tuitionfee = payment_amount
        tuition.unpaid_tuitionfee = str(int(tuition.total_tuitionfee) - int(tuition.paid_tuitionfee))
        tuition.save()

        # Refresh from database
        tuition.refresh_from_db()

        # Verify payment processing
        assert tuition.paid_tuitionfee == payment_amount
        assert tuition.unpaid_tuitionfee == "1050000"  # 2,550,000 - 1,500,000

    def test_duplicate_tuitionfee(self, create_student, create_semester):
        """
        TC06: Kiểm tra ràng buộc không trùng lặp học phí
        - Đầu vào: Tạo 2 bản ghi học phí cho cùng sinh viên và học kỳ
        - Xử lý: Thử tạo bản ghi trùng lặp
        - Đầu ra mong đợi: Raise IntegrityError do vi phạm ràng buộc unique_together
        """
        # Tạo bản ghi học phí đầu tiên
        tuition1 = tuitionfee.objects.create(
            idStd=create_student,
            idSemester=create_semester,
            totalcredit=3,
            total_tuitionfee="2550000",
            paid_tuitionfee="0",
            unpaid_tuitionfee="2550000"
        )

        # Thử tạo bản ghi trùng lặp - kỳ vọng sẽ raise IntegrityError
        with pytest.raises(IntegrityError):
            tuition2 = tuitionfee.objects.create(
                idStd=create_student,
                idSemester=create_semester,
                totalcredit=3,
                total_tuitionfee="2550000",
                paid_tuitionfee="0",
                unpaid_tuitionfee="2550000"
            )

    def test_negative_amount_validation(self, create_student, create_semester):
        """
        TC07: Kiểm tra validation số tiền âm
        - Đầu vào: Học phí với số tiền âm
        - Xử lý: Thử tạo và cập nhật với số tiền âm
        - Đầu ra mong đợi: Raise ValidationError do số tiền không được âm
        """
        from django.core.exceptions import ValidationError

        # Thử tạo học phí với tổng tiền âm
        with pytest.raises(ValidationError):
            tuition = tuitionfee.objects.create(
                idStd=create_student,
                idSemester=create_semester,
                totalcredit=3,
                total_tuitionfee="-2550000",  # Số tiền âm
                paid_tuitionfee="0",
                unpaid_tuitionfee="-2550000"
            )

        # Tạo bản ghi học phí hợp lệ
        tuition = tuitionfee.objects.create(
            idStd=create_student,
            idSemester=create_semester,
            totalcredit=3,
            total_tuitionfee="2550000",
            paid_tuitionfee="0",
            unpaid_tuitionfee="2550000"
        )

        # Thử cập nhật với số tiền đã đóng âm
        with pytest.raises(ValidationError):
            tuition.paid_tuitionfee = "-1000000"  # Số tiền âm
            tuition.full_clean()
            tuition.save()

    def test_negative_credits_validation(self, create_student, create_semester):
        """
        TC08: Kiểm tra validation số tín chỉ âm
        - Đầu vào: Học phí với số tín chỉ âm
        - Xử lý: Thử tạo học phí với số tín chỉ âm
        - Đầu ra mong đợi: Raise ValidationError do số tín chỉ không được âm
        """
        from django.core.exceptions import ValidationError

        # Thử tạo học phí với số tín chỉ âm
        with pytest.raises(ValidationError):
            tuition = tuitionfee.objects.create(
                idStd=create_student,
                idSemester=create_semester,
                totalcredit=-3,  # Số tín chỉ âm
                total_tuitionfee="2550000",
                paid_tuitionfee="0",
                unpaid_tuitionfee="2550000"
            )

    def test_decimal_calculation_precision(self, create_student, create_semester):
        """
        TC09: Kiểm tra độ chính xác của phép tính với số thập phân
        - Đầu vào: Học phí với số tiền thập phân
        - Xử lý: Thực hiện các phép tính với số thập phân
        - Đầu ra mong đợi: Giữ được độ chính xác của số thập phân
        """
        # Tạo học phí với số tiền thập phân
        tuition = tuitionfee.objects.create(
            idStd=create_student,
            idSemester=create_semester,
            totalcredit=3,
            total_tuitionfee="2550000.50",  # Số thập phân
            paid_tuitionfee="1000000.25",   # Số thập phân
            unpaid_tuitionfee="1549999.75"  # = 2550000.50 - 1000000.25
        )

        # Cập nhật số tiền đã đóng với số thập phân
        tuition.paid_tuitionfee = "1500000.30"  # Số thập phân mới
        tuition.unpaid_tuitionfee = str(
            Decimal(tuition.total_tuitionfee) - Decimal(tuition.paid_tuitionfee)
        )
        tuition.save()

        # Kiểm tra độ chính xác của phép tính
        tuition.refresh_from_db()
        # Kiểm tra số tiền chưa đóng = 2550000.50 - 1500000.30 = 1050000.20
        assert Decimal(tuition.unpaid_tuitionfee) == Decimal("1050000.20")
        # Kiểm tra tổng tiền = đã đóng + chưa đóng
        assert Decimal(tuition.total_tuitionfee) == Decimal(tuition.paid_tuitionfee) + Decimal(tuition.unpaid_tuitionfee)

    def test_get_semester_std_success(self, client, create_student, create_semester, create_moduleclass):
        """
        TC10: Kiểm tra lấy danh sách học kỳ của sinh viên
        - Đầu vào: Sinh viên đã đăng ký học phần trong một học kỳ
        - Xử lý: Gọi API get_semester_std
        - Đầu ra mong đợi: Trả về danh sách học kỳ chứa học kỳ đã đăng ký
        """
        # Đăng ký học phần cho sinh viên
        student_moduleclass = Student_ModuleClass.objects.create(
            idStd=create_student,
            module_class=create_moduleclass
        )

        # Login sinh viên
        client.force_login(create_student)

        # Gọi API
        response = client.get(reverse('get_semester_std'))
        
        # Kiểm tra response
        assert response.status_code == 200
        data = json.loads(response.content)
        
        # Kiểm tra cấu trúc dữ liệu
        assert 'semesters' in data
        assert len(data['semesters']) == 1
        
        # Kiểm tra thông tin học kỳ
        semester_data = data['semesters'][0]
        assert semester_data['idSemester'] == create_semester.idSemester
        assert semester_data['nameSemester'] == create_semester.nameSemester

    def test_get_semester_std_no_data(self, client, create_student):
        """
        TC11: Kiểm tra lấy danh sách học kỳ khi sinh viên chưa đăng ký học phần
        - Đầu vào: Sinh viên chưa đăng ký học phần nào
        - Xử lý: Gọi API get_semester_std
        - Đầu ra mong đợi: Trả về thông báo lỗi phù hợp
        """
        # Login sinh viên
        client.force_login(create_student)

        # Gọi API
        response = client.get(reverse('get_semester_std'))
        
        # Kiểm tra response
        assert response.status_code == 200
        data = json.loads(response.content)
        
        # Kiểm tra thông báo lỗi
        assert 'error' in data
        assert data['error'] == "Sinh viên này không có học kỳ nào trong CSDL"

    def test_get_semester_std_multiple_semesters(self, client, create_student, create_moduleclass):
        """
        TC12: Kiểm tra lấy danh sách học kỳ khi sinh viên đăng ký nhiều học kỳ
        - Đầu vào: Sinh viên đăng ký học phần trong nhiều học kỳ
        - Xử lý: Gọi API get_semester_std
        - Đầu ra mong đợi: Trả về danh sách đầy đủ các học kỳ
        """
        # Tạo học kỳ thứ 2
        semester2 = Semester.objects.create(
            idSemester="HK2-23-24",
            nameSemester="Học kỳ 2 năm 2023-2024",
            start_date=date(2024, 2, 1),
            end_date=date(2024, 6, 30)
        )

        # Tạo lớp học phần cho học kỳ 2
        moduleclass2 = ModuleClass.objects.create(
            module=create_moduleclass.module,
            idClass=create_moduleclass.idClass,
            semester=semester2,
            max_slot=40
        )

        # Đăng ký học phần cho sinh viên ở cả 2 học kỳ
        Student_ModuleClass.objects.create(
            idStd=create_student,
            module_class=create_moduleclass
        )
        Student_ModuleClass.objects.create(
            idStd=create_student,
            module_class=moduleclass2
        )

        # Login sinh viên
        client.force_login(create_student)

        # Gọi API
        response = client.get(reverse('get_semester_std'))
        
        # Kiểm tra response
        assert response.status_code == 200
        data = json.loads(response.content)
        
        # Kiểm tra số lượng học kỳ
        assert 'semesters' in data
        assert len(data['semesters']) == 2
        
        # Kiểm tra thông tin các học kỳ
        semester_ids = [sem['idSemester'] for sem in data['semesters']]
        assert create_moduleclass.semester.idSemester in semester_ids
        assert semester2.idSemester in semester_ids
