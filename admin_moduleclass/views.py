from django.shortcuts import render
from login_admin.models import profile_admin
from django.contrib.auth.decorators import login_required
from faculty.models import *
from django.http import JsonResponse
from django.db.models import Q
from course.models import *
from django.forms.models import model_to_dict
from schedule.models import *
import json
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@login_required(login_url='login_admin')
def admin_moduleclass(request):

    getidAdmin = request.user.idAdmin                                           # thong tin admin
    admininfo = profile_admin.objects.get(idAdmin=getidAdmin)
    infoAdmin = {'admininfo': admininfo,}

    return render(request, 'admin_moduleclass.html', infoAdmin)

#lay danh sach khoa
@login_required(login_url='login_admin')
def get_faculty(request):
    faculties = Faculty.objects.all()
    faculties_data = [{'idFaculty': faculty.idFaculty, 'nameFaculty': faculty.nameFaculty} for faculty in faculties]
    return JsonResponse({'faculties': faculties_data})


# lấy danh sách ngành thuộc khoa
@login_required(login_url='login_admin')
def get_department(request, idFaculty):
    departments = Department.objects.filter(faculty = idFaculty)
    departments_data = [{'idDepartment': department.idDepartment, 'nameDepartment': department.nameDepartment} for department in departments]
    return JsonResponse({'departments': departments_data})

#lay danh sach khóa
@login_required(login_url='login_admin')
def get_idCourse(request):
    idCourses = idCourse.objects.all()
    idCourses_data = [{'idCourse': idCourse.idCourse, 'nameCourse': idCourse.nameCourse} for idCourse in idCourses]
    return JsonResponse({'idCourses': idCourses_data})

#lấy danh sách lớp thuộc ngành + khóa
@login_required(login_url='login_admin')
def get_class(request, idDepartment, idCourse):
    classes = FacultyClasses.objects.filter(department = idDepartment, idCourse = idCourse)
    classes_data = [{'idClass': classe.idClass} for classe in classes]
    return JsonResponse({'classes': classes_data})

#tìm lớp
@login_required(login_url='login_admin')
def get_search_class(request ,input_value):
    classes_results = FacultyClasses.objects.filter(
        Q(idClass__icontains = input_value) |
        Q(department__nameDepartment__icontains = input_value) |
        Q(idCourse__nameCourse__icontains = input_value) |
        Q(department__faculty__nameFaculty__icontains = input_value)
    )
    classes_data = [{'idClass': classes.idClass,
                     'department': classes.department.nameDepartment,
                     'faculty': classes.department.faculty.nameFaculty,
                     'idCourse': classes.idCourse.nameCourse } for classes in classes_results]
    return JsonResponse({'classes' :classes_data})



#lấy danh sách môn  học
@login_required(login_url='login_admin')
def get_list_module(request, idClass):
    Department_idClass = FacultyClasses.objects.get(idClass = idClass).department
    unknown_department = Department.objects.get(idDepartment = 'unknown')
    module_departments = Module.objects.filter(
        Q(department = Department_idClass) |
        Q(department = unknown_department)
    )
    module_departments_data = [{'idModule': module_department.idModule, 'nameModule': module_department.nameModule, 'credits': module_department.credits, 'department': module_department.department.nameDepartment} for module_department in module_departments]
    return JsonResponse({'module_departments': module_departments_data})

#lay thong tin mon hoc tu idModule
@login_required(login_url='login_admin')
def get_module_byidModule(request, idModule):
    module = Module.objects.get(idModule=idModule)
    module_data = model_to_dict(module)
    return JsonResponse(module_data)

#lay danh sach phong hoc tu database
@login_required(login_url='login_admin')
def get_room(request):
    rooms = ClassRoom.objects.all()
    rooms_data = [{'idRoom': room.idClassRoom, 'nameRoom': room.nameClassRoom} for room in rooms]
    return JsonResponse({'rooms': rooms_data})


# lay danh sach hoc ky tu database
@login_required(login_url='login_admin')
def get_semester(request):
    semesters = Semester.objects.all()
    semester_data = [{'idSemester': semester.idSemester, 'nameSemester': semester.nameSemester} for semester in semesters]
    return JsonResponse({'semesters': semester_data})


# lay danh sach mon hoc thuoc lop + ky hoc
@login_required(login_url='login_admin')
def get_module_idClass_idSemester(request, idClass, idSemester):
    idClass_instance = FacultyClasses.objects.get(idClass = idClass)
    idSemester_instance = Semester.objects.get(idSemester = idSemester)
    moduleclass = ModuleClass.objects.filter(idClass = idClass_instance, semester = idSemester_instance)
    list_idModule =  moduleclass.values_list('module_id', flat=True)
    list_module = Module.objects.filter(idModule__in=list_idModule)
    modules = [model_to_dict(module) for module in list_module]
    return JsonResponse({'modules': modules})


#check môn học đã lưu trong database  hay chua
@login_required(login_url='login_admin')
def check_moduleclass_exist(request, idClass, idModule):
    try:
        get_moduleclass = ModuleClass.objects.get(idClass__idClass = idClass, module__idModule = idModule)
        return JsonResponse({'exist': True})
    except ModuleClass.DoesNotExist:
        return JsonResponse({'exist': False})


#xoa mon hoc thuoc lop
@login_required(login_url='login_admin')
def delete_moduleclass(request, idClass, idModule):
    response_data ={}
    try:
        moduleclass = ModuleClass.objects.get(idClass__idClass= idClass, module__idModule=idModule)
        moduleclass.delete()
        response_data['result'] = 'deleted'
        return JsonResponse(response_data)
    except ModuleClass.DoesNotExist:
        response_data['result'] = 'delete_failed'
        return JsonResponse(response_data)
    


#lay lich hoc va lich thi tu database
@login_required(login_url='login_admin')
def get_schedule_detail(request, idClass, idModule):
    try:
        moduleclass = ModuleClass.objects.get(idClass__idClass = idClass, module__idModule = idModule)
        max_slot = moduleclass.max_slot
        schedule_list = ScheduleModuleClass.objects.filter(idModuleClass = moduleclass)
        schedule_exam = ScheduleFinalExam.objects.get(idModuleClass = moduleclass)
        schedule_data = [model_to_dict(schedule) for schedule in schedule_list]
        schedule_exam_data = model_to_dict(schedule_exam)
        return JsonResponse({'schedule_data': schedule_data, 'schedule_exam_data': schedule_exam_data, 'max_slot': max_slot})
    except ModuleClass.DoesNotExist:
        return JsonResponse({'exist': 'none'})


# luu thong tin ve lop mon hoc da tao
@login_required(login_url='login_admin')
def save_moduleclass(request, idClass, idModule, idSemester):
    response_data = {}
    if request.method == 'POST':
        data_schedule = json.loads(request.body)
        tableSchedules = data_schedule.get('tableSchedule')
        tableScheduleExam = data_schedule.get('tableScheduleExam')
        max_slot = data_schedule.get('max_slot')

        module_instance = Module.objects.get(idModule = idModule)
        idClass_instance = FacultyClasses.objects.get(idClass = idClass)
        semester_instance = Semester.objects.get(idSemester = idSemester)

        try:
            thisModuleClass = ModuleClass.objects.get(module = module_instance, idClass = idClass_instance)
            thisModuleClass.max_slot = max_slot
            save_Schedule(tableSchedules, thisModuleClass)
            
            save_ScheduleExam(tableScheduleExam, thisModuleClass)
            thisModuleClass.save()
            response_data['result'] = 'updated'
            return JsonResponse(response_data) 
            
        except ModuleClass.DoesNotExist:
            newModuleClass = ModuleClass(
                module = module_instance,
                idClass = idClass_instance,
                semester = semester_instance,
                max_slot = max_slot,
            )
            newModuleClass.save()

            save_Schedule(tableSchedules, newModuleClass)

            save_ScheduleExam(tableScheduleExam, newModuleClass)
        
            response_data['result'] = 'added'
            return JsonResponse(response_data)



#luu thong tin ve lich thi
def save_ScheduleExam(ScheduleExam_data, idModuleClass_data):
    class_room_exam_instance = ClassRoom.objects.get(idClassRoom = ScheduleExam_data[2])
    date_exam_instance = ScheduleExam_data[0]
    if date_exam_instance:
        date_exam_value = date_exam_instance
    else:
        date_exam_value = None
    try:
        thisScheduleExam = ScheduleFinalExam.objects.get(idModuleClass = idModuleClass_data)
        thisScheduleExam.date_exam = date_exam_value
        thisScheduleExam.period_start = ScheduleExam_data[1]
        thisScheduleExam.class_room = class_room_exam_instance
        thisScheduleExam.save()
        print('updated_exam_schedule')
    
    except ScheduleFinalExam.DoesNotExist:
        newScheduleExam = ScheduleFinalExam(
            idModuleClass = idModuleClass_data,
            date_exam = date_exam_value,
            period_start = ScheduleExam_data[1],
            class_room = class_room_exam_instance
        )
        newScheduleExam.save()
        print('added_exam_schedule')


#luu thong tin ve lich hoc
def save_Schedule(Schedule_data, idModuleClass_data):
    try:
        thisScheduleModuleClass = ScheduleModuleClass.objects.filter(idModuleClass = idModuleClass_data)
        if not thisScheduleModuleClass.exists():
            raise ScheduleModuleClass.DoesNotExist
        for schedule in Schedule_data:
            idSMC = schedule[6]
            try:
                schedule_exist = ScheduleModuleClass.objects.get(idSMC = idSMC)
                if schedule[3]:
                    date_start = schedule[3]
                else:
                    date_start = None

                if schedule[4]:
                    date_end = schedule[4]
                else:
                    date_end = None
                
                schedule_exist.days_of_week = schedule[0]
                schedule_exist.period_start = schedule[1]
                schedule_exist.periods_count = schedule[2]
                schedule_exist.start_date = date_start
                schedule_exist.end_date = date_end
                class_room_instance = ClassRoom.objects.get(idClassRoom=schedule[5])
                schedule_exist.class_room = class_room_instance
                schedule_exist.save()
                print('updated_schedule')
            
            except ScheduleModuleClass.DoesNotExist:
                class_room_instance = ClassRoom.objects.get(idClassRoom = schedule[5])
                if schedule[3]:
                    date_start = schedule[3]
                else:
                    date_start = None

                if schedule[4]:
                    date_end = schedule[4]
                else:
                    date_end = None 
                 
                newSchedule = ScheduleModuleClass(
                idModuleClass = idModuleClass_data,
                days_of_week = schedule[0],
                period_start = schedule[1],
                periods_count = schedule[2],
                start_date = date_start,
                end_date = date_end,
                class_room = class_room_instance
                )
                newSchedule.save()
                print('added_schedule')

    except ScheduleModuleClass.DoesNotExist:
        for schedule in  Schedule_data:
            class_room_instance = ClassRoom.objects.get(idClassRoom = schedule[5])
            if schedule[3]:
                date_start = schedule[3]
            else:
                date_start = None

            if schedule[4]:
                date_end = schedule[4]
            else:
                date_end = None   

            newSchedule = ScheduleModuleClass(
                idModuleClass = idModuleClass_data,
                days_of_week = schedule[0],
                period_start = schedule[1],
                periods_count = schedule[2],
                start_date = date_start,
                end_date = date_end,
                class_room = class_room_instance
            )
            newSchedule.save()
            print('added_schedule')



#kiem tra lich hoc va xoa
@login_required(login_url='login_admin')
def delete_schedule(request, idSMC):
    if idSMC != "undefined":
        try:
            schedule = ScheduleModuleClass.objects.get(idSMC=idSMC)
            schedule.delete()
            return JsonResponse({'exist': True})
        except ScheduleModuleClass.DoesNotExist:
            return JsonResponse({'exist': False})
    else:
        return JsonResponse({'exist': False})
     


