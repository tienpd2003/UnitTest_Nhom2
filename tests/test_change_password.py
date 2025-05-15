from django.test import TestCase
from login_std.models import profile_std
from faculty.models import Faculty, Department, idCourse, FacultyClasses
from datetime import date

class ChangePasswordTestCase(TestCase):
    def setUp(self):
        # Tạo dữ liệu liên quan
        faculty = Faculty.objects.create(idFaculty="CNTT", nameFaculty="Công nghệ thông tin")
        department = Department.objects.create(faculty=faculty, idDepartment="CNPM", nameDepartment="Phần mềm")
        course = idCourse.objects.create(idCourse="K22", nameCourse="Khóa 2022")
        class_obj = FacultyClasses.objects.create(idClass="CLC123", department=department, idCourse=course)

        # Tạo sinh viên
        self.student = profile_std.objects.create(
            idStd="1234567890",
            password="123",  # sẽ được mã hóa nhờ signal
            nameStd="Nguyễn Văn A",
            datebirthStd=date(2000, 1, 1),
            genderStd="Nam",
            addressStd="Hà Nội",
            idClass=class_obj
        )

    def test_change_password(self):
        # Kiểm tra mật khẩu cũ đúng
        self.assertTrue(self.student.check_custom_password("123"))

        # Đổi mật khẩu
        self.student.set_custom_password("newpass456")
        self.student.save()

        # Cần refresh lại từ DB để đảm bảo đã lưu
        self.student.refresh_from_db()

        # Mật khẩu cũ không còn đúng
        self.assertFalse(self.student.check_custom_password("123"))

        # Mật khẩu mới đúng
        self.assertTrue(self.student.check_custom_password("newpass456"))
    def test_password_is_hashed(self):
        self.assertNotEqual(self.student.password, '123456')  # không phải plain text

    def test_check_custom_password_success(self):
        self.assertTrue(self.student.check_custom_password('123'))

    def test_check_custom_password_fail(self):
        self.assertFalse(self.student.check_custom_password('wrongpass'))
