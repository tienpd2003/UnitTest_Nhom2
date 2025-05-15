import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from login_std.models import profile_std
from faculty.models import Department, idCourse, FacultyClasses


@pytest.fixture
def create_valid_student():
    """Tạo 1 sinh viên thật sự có trong hệ thống"""
    dept = Department.objects.create(idDep="CNTT", nameDep="Công nghệ thông tin")
    course = idCourse.objects.create(idCourse="K60", nameCourse="Khóa 60 (2015)")
    cls = FacultyClasses.objects.create(idClass="60PM1", department=dept, idCourse=course)

    profile_std.objects.create(
        idStd="222",
        password=make_password("123456"),  # Đây là mật khẩu đúng
        nameStd="aaa",
        datebirthStd="2025-04-22",
        genderStd="Nam",
        identityStd="12312421",
        ethnicityStd="Ha Noi",
        phoneStd="0862386325",
        emailStd="sv@gmail.com",
        addressStd="nghean",
        idClass=cls,
        graduate=True
    )


@pytest.mark.django_db(transaction=True)
def test_login_correct_input(client, create_valid_student):
    response = client.post(reverse('login_std'), {
        "username": "222",
        "password": "123456"
    })

    assert response.status_code == 302
    assert response.url == reverse('profile')


@pytest.mark.django_db(transaction=True)
def test_login_wrong_password(client, create_valid_student):
    response = client.post(reverse('login_std'), {
        "username": "222",
        "password": "5555"
    })

    assert response.status_code == 200
    assert b"Sai th\xc3\xb4ng tin t\xc3\xa0i kho\xe1\xba\xa3n" in response.content


@pytest.mark.django_db(transaction=True)
def test_login_wrong_username(client):
    response = client.post(reverse('login_std'), {
        "username": "999",
        "password": "555"
    })

    assert response.status_code == 200
    assert b"Sai th\xc3\xb4ng tin t\xc3\xa0i kho\xe1\xba\xa3n" in response.content
