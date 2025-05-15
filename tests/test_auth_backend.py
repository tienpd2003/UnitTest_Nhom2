from django.test import TestCase
from django.contrib.auth import authenticate
from login_std.models import profile_std
from login_std.backends import CustomAuthBackendStd
from datetime import date
from faculty.models import Faculty, Department, idCourse, FacultyClasses

class TestCustomAuthBackendStd(TestCase):
    def setUp(self):
        # Tạo dữ liệu mẫu cho các ForeignKey
        faculty = Faculty.objects.create(idFaculty="F001", nameFaculty="Công nghệ thông tin")
        department = Department.objects.create(faculty=faculty, idDepartment="D001", nameDepartment="Khoa học máy tính")
        course = idCourse.objects.create(idCourse="K20", nameCourse="Khóa 2020")
        class_obj = FacultyClasses.objects.create(idClass="IT001", department=department, idCourse=course)

        # Tạo sinh viên với dữ liệu cơ bản
        self.username = "12345"
        self.password = "testpassword"
        self.user_std = profile_std.objects.create(
            idStd=self.username,
            nameStd="Nguyen Van A",
            password=self.password,  # Mật khẩu sẽ được mã hóa tự động nhờ signal
            datebirthStd=date(2000, 1, 1),
            genderStd='Nam',
            addressStd="Ha Noi",
            idClass=class_obj,  # Gán lớp học đã tạo
        )
        self.user_std.set_custom_password(self.password)
        self.user_std.save()

    def test_authenticate_success(self):
        backend = CustomAuthBackendStd()
        user = backend.authenticate(request=None, username=self.username, password=self.password)
        self.assertIsNotNone(user)
        self.assertEqual(user.idStd, self.username)

    def test_authenticate_wrong_username(self):
        user = authenticate(username='wrongusername', password=self.password)
        self.assertIsNone(user)

    def test_authenticate_wrong_password(self):
        user = authenticate(username=self.username, password='wrongpassword')
        self.assertIsNone(user)

    def test_get_user_success(self):
        backend = CustomAuthBackendStd()
        user = backend.get_user(self.user_std.pk)
        self.assertIsNotNone(user)
        self.assertEqual(user.idStd, self.username)

    def test_get_user_not_found(self):
        backend = CustomAuthBackendStd()
        user = backend.get_user(99999)
        self.assertIsNone(user)
