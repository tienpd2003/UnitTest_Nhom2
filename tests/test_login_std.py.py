import pytest
from login_std.backends import CustomAuthBackendStd
from login_std.models import profile_std


@pytest.mark.django_db
def test_authenticate_correct_credentials():
    backend = CustomAuthBackendStd()
    user = backend.authenticate(request=None, username="222", password="123456")
    assert user is not None
    assert isinstance(user, profile_std)
    assert user.idStd == "222"
    print("✅ MSSV đúng + mật khẩu đúng: PASS")


@pytest.mark.django_db
def test_authenticate_wrong_password():
    backend = CustomAuthBackendStd()
    user = backend.authenticate(request=None, username="222", password="sai_mat_khau")
    assert user is None
    print("MSSV đúng + mật khẩu sai: PASS (trả về None)")


@pytest.mark.django_db
def test_authenticate_user_not_found():
    backend = CustomAuthBackendStd()
    user = backend.authenticate(request=None, username="999", password="anything")
    assert user is None
    print("✅ MSSV không tồn tại: PASS (trả về None)")
