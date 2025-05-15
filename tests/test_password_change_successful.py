import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_password_change_successful(client):
    # Tạo user
    user = User.objects.create_user(username='888888', password='oldpassword')

    # Đăng nhập
    client.login(username='888888', password='oldpassword')

    # Gọi API đổi mật khẩu (ví dụ đang dùng url name là 'password_change')
    response = client.post(reverse('password_change'), {
        'old_password': 'oldpassword',
        'new_password1': 'newstrongpass123',
        'new_password2': 'newstrongpass123',
    })

    # Kiểm tra đổi mật khẩu thành công và có redirect
    assert response.status_code == 302

    # Refresh user từ database và kiểm tra mật khẩu mới hoạt động
    user.refresh_from_db()
    assert user.check_password('newstrongpass123')

    # Sau test này database sẽ rollback tự động do `@pytest.mark.django_db`
