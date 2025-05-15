import pytest
from datetime import date
from django.contrib.auth.hashers import make_password, check_password
from login_std.models import profile_std
from login_std.backends import CustomAuthBackendStd
from faculty.models import Faculty, Department, idCourse, FacultyClasses


@pytest.fixture
def setup_test_data(db):
    from login_std.models import profile_std
    from django.contrib.auth.hashers import check_password

    # ForeignKey setup
    faculty = Faculty.objects.create(idFaculty="CNTT", nameFaculty="Công nghệ thông tin")
    department = Department.objects.create(faculty=faculty, idDepartment="PM", nameDepartment="Công nghệ phần mềm")
    course = idCourse.objects.create(idCourse="60", nameCourse="Khóa 60 (2015)")
    class_obj = FacultyClasses.objects.create(idClass="60PM1", department=department, idCourse=course)

    # Tạo sinh viên
    student = profile_std.objects.create(
        idStd="222",
        nameStd="Nguyễn Văn A",
        password=make_password("123456"),
        datebirthStd=date(2000, 1, 1),
        genderStd='Nam',
        addressStd='Hà Nội',
        idClass=class_obj
    )

    # Gán trực tiếp hàm vào INSTANCE (chỉ instance student có)
    def check_pw(self, raw_password):
        print(">>> GỌI check_custom_password với:", raw_password)
        print(">>> hash stored:", self.password)
        return check_password(raw_password, self.password)

    student.check_custom_password = check_pw.__get__(student, profile_std)  # bind đúng instance
    return student


@pytest.mark.django_db
def test_authenticate_success(setup_test_data):
    backend = CustomAuthBackendStd()
    authenticated_user = backend.authenticate(request=None, username='222', password='123456')

    if authenticated_user:
        print("mật khẩu đúng, tên đăng nhập đúng")
        print("Tên sinh viên:", authenticated_user.nameStd)
    else:
        print("❌ Sai kết quả")

    assert authenticated_user is not None
    assert authenticated_user.idStd == '222'



@pytest.mark.django_db
def test_authenticate_wrong_password(setup_test_data):
    backend = CustomAuthBackendStd()
    result = backend.authenticate(request=None, username='222', password='sai_password')

    if result is None:
        print("mật khẩu sai")
    else:
        print("❌ Sai kết quả")

    assert result is None


@pytest.mark.django_db
def test_authenticate_user_not_found():
    backend = CustomAuthBackendStd()
    result = backend.authenticate(request=None, username='khong_tontai', password='abc')

    if result is None:
        print("tên đăng nhập sai")
    else:
        print("❌ Sai kết quả")

    assert result is None


@pytest.mark.django_db
def test_get_user_success(setup_test_data):
    backend = CustomAuthBackendStd()
    result = backend.get_user('222')

    if result:
        print(f"Trả về name sinh viên: {result.nameStd}")
    else:
        print("❌ Sai kết quả")

    assert result is not None
    assert result.idStd == '222'


@pytest.mark.django_db
def test_get_user_not_found():
    backend = CustomAuthBackendStd()
    result = backend.get_user('00000000')

    if result is None:
        print("Sai mã sinh viên")
    else:
        print("❌ Sai kết quả")

    assert result is None
