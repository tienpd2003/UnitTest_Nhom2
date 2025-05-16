import pytest
from datetime import date
from login_admin.models import profile_admin
from login_admin.backends import CustomAuthBackendAdmin

# ======= FIXTURE1: Tạo admin để test =========
@pytest.fixture
def setup_admin_data(db):
    # Gán mật khẩu raw — để signal pre_save mã hóa tự động
    admin = profile_admin.objects.create(
        idAdmin='admin01',
        nameAdmin='Trần Quang Huy',
        password='adminpass123',
        datebirthAdmin=date(1990, 5, 15),
        genderAdmin='Nam',
        phoneAdmin='0905123456',
        emailAdmin='admin@example.com',
        addressAdmin='TP.HCM'
    )
    return admin


# ======= TESTCASE1: Đăng nhập đúng =========
@pytest.mark.django_db
def test_admin_authenticate_success(setup_admin_data):
    backend = CustomAuthBackendAdmin()
    authenticated_user = backend.authenticate(request=None, username='admin01', password='adminpass123')

    assert authenticated_user is not None
    assert authenticated_user.idAdmin == 'admin01'


# =======TESTCASE2: Mật khẩu sai =========
@pytest.mark.django_db
def test_admin_authenticate_wrong_password(setup_admin_data):
    backend = CustomAuthBackendAdmin()
    result = backend.authenticate(request=None, username='admin01', password='wrongpass')

    assert result is None


# ======= TESTCASE3: Người dùng không tồn tại =========
@pytest.mark.django_db
def test_admin_authenticate_user_not_found():
    backend = CustomAuthBackendAdmin()
    result = backend.authenticate(request=None, username='khongtontai', password='123456')

    assert result is None


# ======= TESTCASE4: get_user thành công =========
@pytest.mark.django_db
def test_admin_get_user_success(setup_admin_data):
    backend = CustomAuthBackendAdmin()
    result = backend.get_user(setup_admin_data.pk)

    assert result is not None
    assert result.idAdmin == 'admin01'


# ======= TESTCASE5: get_user không tồn tại =========
@pytest.mark.django_db
def test_admin_get_user_not_found():
    backend = CustomAuthBackendAdmin()
    result = backend.get_user('nonexistent')

    assert result is None
