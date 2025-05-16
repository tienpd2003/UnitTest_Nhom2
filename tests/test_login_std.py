import pytest
from datetime import date
from login_std.models import profile_std
from login_std.backends import CustomAuthBackendStd
from faculty.models import Faculty, Department, idCourse, FacultyClasses

# ======= FIXTURE tạo dữ liệu test =========
@pytest.fixture
def setup_test_data(db):
    faculty = Faculty.objects.create(idFaculty="CNTT", nameFaculty="Công nghệ thông tin")
    department = Department.objects.create(faculty=faculty, idDepartment="PM", nameDepartment="Công nghệ phần mềm")
    course = idCourse.objects.create(idCourse="60", nameCourse="Khóa 60 (2015)")
    class_obj = FacultyClasses.objects.create(idClass="60PM1", department=department, idCourse=course)

    # Gán mật khẩu dạng raw, để pre_save tự động mã hóa
    student = profile_std.objects.create(
        idStd='222',
        nameStd="Nguyễn Văn A",
        password='123456',  # Raw password — sẽ được mã hóa tự động bởi pre_save
        datebirthStd=date(2000, 1, 1),
        genderStd='Nam',
        addressStd='Hà Nội',
        idClass=class_obj
    )
    return student


# ======= TEST: Đăng nhập đúng =========
@pytest.mark.django_db
def test_authenticate_success(setup_test_data):
    backend = CustomAuthBackendStd()
    authenticated_user = backend.authenticate(request=None, username='222', password='123456')

    assert authenticated_user is not None
    assert authenticated_user.idStd == '222'

# ======= TEST: Mật khẩu sai =========
@pytest.mark.django_db
def test_authenticate_wrong_password(setup_test_data):
    backend = CustomAuthBackendStd()
    result = backend.authenticate(request=None, username='222', password='sai_password')

    assert result is None

# ======= TEST: Người dùng không tồn tại =========
@pytest.mark.django_db
def test_authenticate_user_not_found():
    backend = CustomAuthBackendStd()
    result = backend.authenticate(request=None, username='khong_tontai', password='abc')

    assert result is None

# ======= TEST: get_user thành công =========
@pytest.mark.django_db
def test_get_user_success(setup_test_data):
    backend = CustomAuthBackendStd()
    result = backend.get_user(setup_test_data.pk)

    assert result is not None
    assert result.idStd == '222'

# ======= TEST: get_user không tồn tại =========
@pytest.mark.django_db
def test_get_user_not_found():
    backend = CustomAuthBackendStd()
    result = backend.get_user('00000000')  # ID không tồn tại

    assert result is None
