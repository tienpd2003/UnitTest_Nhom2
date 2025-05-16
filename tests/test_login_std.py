import pytest
from datetime import date
from login_std.models import profile_std
from login_std.backends import CustomAuthBackendStd
from faculty.models import Faculty, Department, idCourse, FacultyClasses

# ================= FIXTURE: Tạo dữ liệu test người dùng sinh viên =================
@pytest.fixture
def setup_test_data(db):
    # Tạo dữ liệu mô phỏng: khoa, bộ môn, khóa học, lớp học
    faculty = Faculty.objects.create(idFaculty="CNTT", nameFaculty="Công nghệ thông tin")
    department = Department.objects.create(faculty=faculty, idDepartment="PM", nameDepartment="Công nghệ phần mềm")
    course = idCourse.objects.create(idCourse="60", nameCourse="Khóa 60 (2015)")
    class_obj = FacultyClasses.objects.create(idClass="60PM1", department=department, idCourse=course)

    # Tạo tài khoản sinh viên (id: 222, mật khẩu: 123456)
    # Gán password dưới dạng raw, pre_save signal sẽ tự mã hóa
    student = profile_std.objects.create(
        idStd='222',
        nameStd="Nguyễn Văn A",
        password='123456',  # raw password
        datebirthStd=date(2000, 1, 1),
        genderStd='Nam',
        addressStd='Hà Nội',
        idClass=class_obj
    )
    return student


# ================= TEST CASE 1: Đăng nhập thành công =================
@pytest.mark.django_db
def test_authenticate_success(setup_test_data):
    """
    ✅ Kiểm tra rằng người dùng với thông tin đúng (idStd + mật khẩu) có thể đăng nhập thành công.
    """
    backend = CustomAuthBackendStd()
    authenticated_user = backend.authenticate(request=None, username='222', password='123456')

    assert authenticated_user is not None
    assert authenticated_user.idStd == '222'


# ================= TEST CASE 2: Sai mật khẩu =================
@pytest.mark.django_db
def test_authenticate_wrong_password(setup_test_data):
    """
    ❌ Kiểm tra rằng nếu mật khẩu sai, hệ thống sẽ không xác thực người dùng.
    """
    backend = CustomAuthBackendStd()
    result = backend.authenticate(request=None, username='222', password='sai_password')

    assert result is None


# ================= TEST CASE 3: Tài khoản không tồn tại =================
@pytest.mark.django_db
def test_authenticate_user_not_found():
    """
    ❌ Kiểm tra khi nhập mã sinh viên không tồn tại trong hệ thống → không đăng nhập được.
    """
    backend = CustomAuthBackendStd()
    result = backend.authenticate(request=None, username='khong_tontai', password='abc')

    assert result is None


# ================= TEST CASE 4: Truy xuất người dùng theo ID thành công =================
@pytest.mark.django_db
def test_get_user_success(setup_test_data):
    """
    ✅ Kiểm tra `get_user(id)` trả về đúng đối tượng người dùng nếu ID tồn tại.
    """
    backend = CustomAuthBackendStd()
    result = backend.get_user(setup_test_data.pk)

    assert result is not None
    assert result.idStd == '222'


# ================= TEST CASE 5: Truy xuất người dùng không tồn tại =================
@pytest.mark.django_db
def test_get_user_not_found():
    """
    ❌ Kiểm tra `get_user(id)` trả về None nếu ID không tồn tại trong hệ thống.
    """
    backend = CustomAuthBackendStd()
    result = backend.get_user('00000000')  # ID không tồn tại

    assert result is None
