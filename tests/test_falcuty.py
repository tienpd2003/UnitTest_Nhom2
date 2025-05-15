import pytest
from login_std.backends import CustomAuthBackendStd
from login_std.models import profile_std
from faculty.models import Department, idCourse, FacultyClasses
from django.contrib.auth.hashers import make_password


@pytest.fixture
def valid_student():
    """Tạo 1 sinh viên với MSSV='222' và mật khẩu='matkhau123'"""
    dept = Department.objects.create(idDep="CNTT", nameDep="Công nghệ thông tin")
    course = idCourse.objects.create(idCourse="K60", nameCourse="Khóa 60")
    cls = FacultyClasses.objects.create(idClass="60PM1", department=dept, idCourse=course)

    return profile_std.objects.create(
        idStd="222",
        password=make_password("matkhau123"),
        nameStd="Nguyen Van A",
        datebirthStd="2000-01-01",
        genderStd="Nam",
        identityStd="123456789",
        ethnicityStd="Kinh",
        phoneStd="0912345678",
        emailStd="sv@gmail.com",
        addressStd="Hà Nội",
        idClass=cls,
        graduate=True
    )


@pytest.mark.django_db(transaction=True)
def test_authenticate_success(valid_student):
    """✅ Đăng nhập đúng thông tin"""
    backend = CustomAuthBackendStd()
    user = backend.authenticate(request=None, username="222", password="matkhau123")

    assert user is not None
    assert user.idStd == "222"


@pytest.mark.django_db(transaction=True)
def test_authenticate_wrong_password(valid_student):
    """❌ Sai mật khẩu"""
    backend = CustomAuthBackendStd()
    user = backend.authenticate(request=None, username="222", password="sai_mat_khau")

    assert user is None


@pytest.mark.django_db(transaction=True)
def test_authenticate_user_not_found():
    """❌ MSSV không tồn tại"""
    backend = CustomAuthBackendStd()
    user = backend.authenticate(request=None, username="999", password="batky")

    assert user is None
