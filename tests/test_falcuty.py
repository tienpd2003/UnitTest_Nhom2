import pytest
from django.contrib.auth.models import User
from faculty.models import Faculty, Department, FacultyClasses
from course.models import idCourse
from schedule.models import (
    Module, ModuleClass, Semester, ClassRoom,
    ScheduleFinalExam, ScheduleModuleClass
)
from django.test import RequestFactory
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from views import (
    get_search_class, check_moduleclass_exist, delete_moduleclass,
    delete_schedule, save_moduleclass, get_schedule_detail, get_module_byidModule
)

# ==== TẠO DỮ LIỆU MẪU ====

@pytest.fixture
def sample_data(db):
    faculty = Faculty.objects.create(idFaculty='CNTT', nameFaculty='Công nghệ thông tin')
    department = Department.objects.create(idDepartment='PM', nameDepartment='Công nghệ phần mềm', faculty=faculty)
    unknown_department = Department.objects.create(idDepartment='unknown', nameDepartment='Unknown', faculty=faculty)
    course = idCourse.objects.create(idCourse='61', nameCourse='Khóa 61 (2016)')
    faculty_class = FacultyClasses.objects.create(idClass='61PM1', department=department, idCourse=course)
    module = Module.objects.create(idModule='"250101"', nameModule='"Vật lý 1"', credits=3, department=department)
    semester = Semester.objects.create(idSemester='"2023B"', nameSemester='"HK II - 2023"')
    room = ClassRoom.objects.create(idClassRoom='"H1.101"', nameClassRoom='"H1.101"')
    user = User.objects.create_user(username='555', password='1')
    
    return {
        'faculty': faculty,
        'department': department,
        'unknown_department': unknown_department,
        'course': course,
        'faculty_class': faculty_class,
        'module': module,
        'semester': semester,
        'room': room,
        'user': user
    }

@pytest.fixture
def rf():
    return RequestFactory()

# ==== TEST CÁC VIEW ====

def test_get_search_class(rf, sample_data):
    req = rf.get('/search/CL01')
    req.user = sample_data['user']
    res = get_search_class(req, "CL01")
    assert isinstance(res, JsonResponse)
    assert res.status_code == 200
    assert 'classes' in res.json()

def test_check_moduleclass_exist_view(rf, sample_data):
    ModuleClass.objects.create(
        idClass=sample_data['faculty_class'],
        module=sample_data['module'],
        semester=sample_data['semester'],
        max_slot=10
    )
    req = rf.get('/')
    req.user = sample_data['user']
    res = check_moduleclass_exist(req, "CL01", "M01")
    assert res.status_code == 200
    assert res.json()['exist'] is True

def test_delete_moduleclass(rf, sample_data):
    ModuleClass.objects.create(
        idClass=sample_data['faculty_class'],
        module=sample_data['module'],
        semester=sample_data['semester'],
        max_slot=10
    )
    req = rf.get('/')
    req.user = sample_data['user']
    res = delete_moduleclass(req, "CL01", "M01")
    assert res.status_code == 200
    assert res.json()['result'] == 'deleted'

def test_delete_schedule(rf, sample_data):
    moduleclass = ModuleClass.objects.create(
        idClass=sample_data['faculty_class'],
        module=sample_data['module'],
        semester=sample_data['semester'],
        max_slot=5
    )
    schedule = ScheduleModuleClass.objects.create(
        idModuleClass=moduleclass,
        days_of_week='Monday',
        period_start=1,
        periods_count=2,
        class_room=sample_data['room']
    )
    req = rf.get('/')
    req.user = sample_data['user']
    res = delete_schedule(req, schedule.idSMC)
    assert res.status_code == 200
    assert res.json()['exist'] is True

def test_save_moduleclass_create_new(rf, sample_data):
    data = {
        "tableSchedule": [
            ["Monday", 1, 2, "2025-06-01", "2025-06-15", "R1", ""]
        ],
        "tableScheduleExam": ["2025-06-20", 1, "R1"],
        "max_slot": 10
    }
    req = rf.post('/', content_type='application/json', data=data)
    req.user = sample_data['user']
    import json
    req._body = json.dumps(data).encode('utf-8')

    res = save_moduleclass(req, "CL01", "M01", "S1")
    assert res.status_code == 200
    assert res.json()['result'] == 'added'

def test_get_schedule_detail(rf, sample_data):
    moduleclass = ModuleClass.objects.create(
        idClass=sample_data['faculty_class'],
        module=sample_data['module'],
        semester=sample_data['semester'],
        max_slot=10
    )
    ScheduleFinalExam.objects.create(
        idModuleClass=moduleclass,
        date_exam="2025-06-30",
        period_start=1,
        class_room=sample_data['room']
    )
    ScheduleModuleClass.objects.create(
        idModuleClass=moduleclass,
        days_of_week="Tuesday",
        period_start=2,
        periods_count=2,
        start_date="2025-06-01",
        end_date="2025-06-30",
        class_room=sample_data['room']
    )

    req = rf.get('/')
    req.user = sample_data['user']
    res = get_schedule_detail(req, "CL01", "M01")
    assert res.status_code == 200
    assert 'schedule_data' in res.json()
    assert 'schedule_exam_data' in res.json()

def test_get_module_byidModule(rf, sample_data):
    req = rf.get('/')
    req.user = sample_data['user']
    res = get_module_byidModule(req, "M01")
    assert res.status_code == 200
    assert 'nameModule' in res.json()
