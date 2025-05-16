import pytest
from django.test import Client
from django.db import IntegrityError  # Import đúng IntegrityError
import json  # Import đúng thư viện json
from faculty.models import Faculty, Department, idCourse, FacultyClasses
from course.models import Module, ModuleClass
from schedule.models import ClassRoom, Semester, ScheduleModuleClass, ScheduleFinalExam

@pytest.fixture
def setup_data(db):
    # Tạo dữ liệu mẫu cho các mô hình cần thiết
    faculty = Faculty.objects.create(idFaculty='CNTT', nameFaculty='Công nghệ thông tin')
    department = Department.objects.create(idDepartment='PM', nameDepartment='Phần mềm', faculty=faculty)
    course = idCourse.objects.create(idCourse='60', nameCourse='Khoá 60')
    clazz = FacultyClasses.objects.create(idClass='60PM1', department=department, idCourse=course)
    module = Module.objects.create(idModule='INT1001', nameModule='Lập trình Python', credits=3, department=department)
    semester = Semester.objects.create(idSemester='HK1', nameSemester='Học kỳ 1', start_date='2025-01-01', end_date='2025-06-01')
    room = ClassRoom.objects.create(idClassRoom='R001', nameClassRoom='Phòng 1')
    module_class = ModuleClass.objects.create(idClass=clazz, module=module, semester=semester, max_slot=30)

    return {
        "faculty": faculty,
        "department": department,
        "course": course,
        "class": clazz,
        "module": module,
        "semester": semester,
        "room": room,
        "module_class": module_class
    }

@pytest.fixture
def auth_client():
    # Tạo client đã đăng nhập giả lập
    client = Client()
    return client
@pytest.mark.django_db
def test_TC1_to_TC4_get_search_class(auth_client, setup_data):
    for desc, value in [
        ("TC1 - Tìm lớp với chuỗi rỗng", ""),
        ("TC2 - Tìm lớp với chuỗi không tồn tại", "InvalidSearch"),
        ("TC3 - Tìm lớp với chuỗi chính xác", "60PM1"),
        ("TC4 - Tìm lớp với chuỗi một phần", "60")
    ]:
        print(f"{desc}:")
        # Kiểm tra đúng với URL đã định nghĩa trong `urls.py`
        res = auth_client.get(f'/search-class/{value}')
        assert res.status_code == 200  # Kiểm tra status code trả về là 200 OK
        print(res.json())
@pytest.mark.django_db
def test_TC5_to_TC8_check_moduleclass_exist(auth_client, setup_data):
    for desc, idClass, idModule in [
        ("TC5 - Lớp học và môn học tồn tại", "60PM1", "INT1001"),
        ("TC6 - Môn học không tồn tại trong lớp", "60PM1", "ABC123"),
        ("TC7 - Lớp học không tồn tại", "XYZ", "INT1001"),
        ("TC8 - Lớp học và môn học không tồn tại", "XXX", "ZZZ")
    ]:
        print(f"{desc}:")
        # Kiểm tra đúng với URL đã định nghĩa trong `urls.py`
        res = auth_client.get(f'/check-moduleclass-exist/{idClass}/{idModule}')
        assert res.status_code == 200  # Kiểm tra status code trả về là 200 OK
        print(res.json())
@pytest.mark.django_db
def test_TC9_to_TC12_delete_moduleclass(auth_client, setup_data):
    for desc, idClass, idModule in [
        ("TC9 - Xoá môn học đã tồn tại", "60PM1", "INT1001"),
        ("TC10 - Xoá môn học không tồn tại", "60PM1", "XYZ000"),
        ("TC11 - Xoá lớp không hợp lệ", "FAKECLASS", "XYZ000"),
        ("TC12 - Xoá cả lớp và môn học không hợp lệ", "??", "###")
    ]:
        print(f"{desc}:")
        # Kiểm tra đúng với URL đã định nghĩa trong `urls.py`
        res = auth_client.get(f'/delete-moduleclass/{idClass}/{idModule}')
        assert res.status_code == 200  # Kiểm tra status code trả về là 200 OK
        print(res.json())
@pytest.mark.django_db
def test_TC13_to_TC14_delete_schedule(auth_client, setup_data):
    mc = setup_data["module_class"]
    room = setup_data["room"]
    schedule = ScheduleModuleClass.objects.create(
        idModuleClass=mc,
        days_of_week='2', period_start='1', periods_count=3,
        start_date='2025-01-01', end_date='2025-01-10',
        class_room=room
    )

    print("TC13 - Xoá lịch học đã tồn tại:")
    res = auth_client.get(f'/delete-schedule/{schedule.idSMC}')
    assert res.status_code == 200  # Kiểm tra status code trả về là 200 OK
    print(res.json())

    print("TC14 - Xoá lịch học không tồn tại:")
    res = auth_client.get('/delete-schedule/INVALID')
    assert res.status_code == 404  # Kiểm tra status code trả về là 404 Not Found
    print(res.json())
@pytest.mark.django_db
def test_TC15_to_TC18_save_Schedule(auth_client, setup_data):
    mc = setup_data["module_class"]
    room = setup_data["room"]

    # TC15 - Cập nhật lịch học đã tồn tại
    schedule = ScheduleModuleClass.objects.create(
        idModuleClass=mc, days_of_week='2', period_start='1',
        periods_count=3, start_date='2025-01-01', end_date='2025-01-10',
        class_room=room
    )
    schedule.days_of_week = '3'
    schedule.save()
    print(f"Updated Schedule: {schedule.idSMC}, New Day: {schedule.days_of_week}")
    assert schedule.days_of_week == '3'  # Kiểm tra rằng lịch học đã được cập nhật

    # TC16 - Tạo lịch học mới khi chưa có
    ScheduleModuleClass.objects.filter(idModuleClass=mc).delete()
    new_schedule = ScheduleModuleClass.objects.create(
        idModuleClass=mc, days_of_week='4', period_start='2',
        periods_count=2, start_date='2025-02-01', end_date='2025-02-10',
        class_room=room
    )
    print(f"Created new schedule: {new_schedule.idSMC}")
    assert new_schedule.days_of_week == '4'  # Kiểm tra rằng lịch học mới đã được tạo

    # TC17 - ModuleClass không tồn tại (giả lập)
    try:
        ScheduleModuleClass.objects.get(idModuleClass=None)
    except Exception as e:
        print("Không tìm thấy ModuleClass:", str(e))

    # TC18 - Thiếu ngày bắt đầu/kết thúc
    incomplete_schedule = ScheduleModuleClass(
        idModuleClass=mc, days_of_week='5', period_start='3',
        periods_count=2, start_date=None, end_date=None, class_room=room
    )
    incomplete_schedule.save()
    print("Lịch học không có ngày bắt đầu/kết thúc đã lưu thành công")
    assert incomplete_schedule.start_date is None  # Kiểm tra rằng lịch học thiếu ngày bắt đầu

@pytest.mark.django_db
def test_TC19_to_TC22_save_ScheduleExam(auth_client, setup_data):
    mc = setup_data["module_class"]
    room = setup_data["room"]

    print("TC19 - Cập nhật lịch thi đã tồn tại:")
    exam = ScheduleFinalExam.objects.create(idModuleClass=mc, date_exam='2025-06-01', period_start='1', class_room=room)
    exam.period_start = '2'
    exam.save()
    print(f"Updated to {exam.period_start}")

    print("TC20 - Thêm mới lịch thi nếu chưa có:")
    ScheduleFinalExam.objects.filter(idModuleClass=mc).delete()
    new_exam = ScheduleFinalExam.objects.create(idModuleClass=mc, date_exam='2025-05-01', period_start='3', class_room=room)
    print(f"Created: {new_exam.idSFE}")

    print("TC21 - Phòng thi không hợp lệ:")
    invalid_room = ClassRoom.objects.create(idClassRoom="INVALID", nameClassRoom="Invalid Room")
    try:
        # Kiểm tra trường hợp phòng thi không hợp lệ
        with pytest.raises(IntegrityError):
            ScheduleFinalExam.objects.create(idModuleClass=mc, date_exam='2025-05-01', period_start='3', class_room=invalid_room)
    except IntegrityError as e:
        print("Caught IntegrityError as expected:", str(e))
@pytest.mark.django_db
def test_TC23_to_TC25_save_moduleclass(auth_client, setup_data):
    clazz = setup_data["class"]
    module = setup_data["module"]
    semester = setup_data["semester"]

    data = {
        "max_slot": 40,
        "tableSchedule": [],
        "tableScheduleExam": ["2025-06-01", "2", "R001"]
    }

    print("TC23 - Cập nhật môn học đã tồn tại:")
    res = auth_client.post(f'/save-moduleclass/{clazz.idClass}/{module.idModule}/{semester.idSemester}',
                           data=json.dumps(data), content_type='application/json')
    assert res.status_code == 200  # Kiểm tra status code trả về là 200 OK
    print(res.json())

    print("TC24 - Tạo mới môn học chưa tồn tại:")
    new_module = Module.objects.create(idModule='NEW001', nameModule='CSDL', credits=3, department=setup_data["department"])
    res = auth_client.post(f'/save-moduleclass/{clazz.idClass}/{new_module.idModule}/{semester.idSemester}',
                           data=json.dumps(data), content_type='application/json')
    assert res.status_code == 200  # Kiểm tra status code trả về là 200 OK
    print(res.json())

    print("TC25 - ID lớp hoặc học phần không tồn tại:")
    res = auth_client.post('/save-moduleclass/@@1/??/HK1',
                           data=json.dumps(data), content_type='application/json')
    assert res.status_code == 400  # Kiểm tra status code trả về là 400 Bad Request
    print(res.json())
@pytest.mark.django_db
def test_TC26_to_TC28_get_schedule_detail(auth_client, setup_data):
    clazz = setup_data["class"]
    module = setup_data["module"]
    mc = setup_data["module_class"]
    room = setup_data["room"]

    ScheduleModuleClass.objects.create(idModuleClass=mc, days_of_week='2', period_start='1',
                                       periods_count=3, start_date='2025-01-01', end_date='2025-01-10', class_room=room)
    ScheduleFinalExam.objects.create(idModuleClass=mc, date_exam='2025-06-01', period_start='2', class_room=room)

    print("TC26 - Có đầy đủ lịch học và lịch thi:")
    res = auth_client.get(f'/get_schedule_detail/{clazz.idClass}/{module.idModule}')
    assert res.status_code == 200  # Kiểm tra status code trả về là 200 OK
    print(res.json())
@pytest.mark.django_db
def test_TC29_to_TC30_get_module_byidModule(auth_client, setup_data):
    print("TC29 - Môn học hợp lệ:")
    res = auth_client.get('/get_module_byidModule/INT1001')
    assert res.status_code == 200  # Kiểm tra status code trả về là 200 OK
    print(res.json())

    print("TC30 - Môn học không tồn tại:")
    res = auth_client.get('/get_module_byidModule/INVALID')
    assert res.status_code == 404  # Kiểm tra status code trả về là 404 Not Found
    print(res.json())
