import pytest
from datetime import date
from django.contrib.auth.hashers import make_password, check_password
from login_admin.models import profile_admin
from login_admin.backends import CustomAuthBackendAdmin  # giả định đã có backend này

@pytest.fixture
def setup_admin_test_data(db):
    # Tạo admin test
    admin = profile_admin.objects.create(
        idAdmin="555",
        nameAdmin="Nguyễn Văn Admin",
        password=make_password("1"),
        datebirthAdmin=date(1985, 5, 15),
        genderAdmin='Nam',
        addressAdmin='Hà Nội'
    )

    # Monkey patch method kiểm tra mật khẩu
    def check_custom_password(self, raw_password):
        return check_password(raw_password, self.password)

    profile_admin.check_custom_password = check_custom_password
    return admin


@pytest.mark.django_db
def test_admin_authenticate_success(setup_admin_test_data):
    backend = CustomAuthBackendAdmin()
    user = backend.authenticate(request=None, username="admin001", password="adminpass")

    if user:
        print("✅ Đăng nhập thành công:", user.nameAdmin)
    else:
        print("❌ Sai kết quả")

    assert user is not None
    assert user.idAdmin == "admin001"


@pytest.mark.django_db
def test_admin_authenticate_wrong_password(setup_admin_test_data):
    backend = CustomAuthBackendAdmin()
    result = backend.authenticate(request=None, username="admin001", password="wrongpass")

    if result is None:
        print("✅ Mật khẩu sai → Không đăng nhập")
    else:
        print("❌ Đăng nhập sai vẫn thành công")

    assert result is None


@pytest.mark.django_db
def test_admin_authenticate_not_found():
    backend = CustomAuthBackendAdmin()
    result = backend.authenticate(request=None, username="notexist", password="whatever")

    if result is None:
        print("✅ Tài khoản không tồn tại")
    else:
        print("❌ Sai kết quả")

    assert result is None


@pytest.mark.django_db
def test_get_admin_success(setup_admin_test_data):
    backend = CustomAuthBackendAdmin()
    result = backend.get_user("admin001")

    if result:
        print("✅ Tìm thấy admin:", result.nameAdmin)
    else:
        print("❌ Không tìm thấy admin")

    assert result is not None
    assert result.idAdmin == "admin001"


@pytest.mark.django_db
def test_get_admin_not_found():
    backend = CustomAuthBackendAdmin()
    result = backend.get_user("unknownadmin")

    if result is None:
        print("✅ Không tồn tại admin")
    else:
        print("❌ Sai kết quả")

    assert result is None
