import json
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from login_std.models import profile_std
from course.models import *
from schedule.models import *
from datetime import datetime
from django.db.models import Q
# Create your views here.


#global variables
global_semester = None

#load page schedule
@login_required(login_url='login_std')
def schedule_view(request):

    current_time = datetime.now()
    current_date = current_time.date()

    getidStd = request.user.idStd
    std_info = profile_std.objects.get(idStd=getidStd)
    stdinfo = {'stdinfo': std_info}
    
    all_semester = Semester.objects.all()

    for semester in all_semester:
        start_date = semester.start_date
        end_date = semester.end_date
        if start_date <= current_date <= end_date:
            idSemester = semester.idSemester
            global global_semester
            global_semester = idSemester


    return render(request, 'schedule.html', stdinfo)



#lay danh sach mon hoc thuoc hoc ky va lich hoc tuong  ung
@login_required(login_url='login_std')
def get_moduleclass_schedule(request, idStd):
    try:
        std = profile_std.objects.get(idStd = idStd)
        global global_semester
        this_semester = global_semester
        transcripts = Student_ModuleClass.objects.filter(idStd = std, module_class__semester = this_semester)
        if not transcripts.exists():
            raise Student_ModuleClass.DoesNotExist
        
        id_moduleclasses = transcripts.values_list('module_class', flat= True).distinct()

        data = []
        for id_moduleclass in id_moduleclasses:
            moduleclass = ModuleClass.objects.get(idModuleClass=id_moduleclass)
            list_schedule = ScheduleModuleClass.objects.filter(idModuleClass = id_moduleclass)
            schedule_exam = ScheduleFinalExam.objects.get(idModuleClass = id_moduleclass)

            moduleclass_data = {
                'nameModule': moduleclass.module.idModule+"-"+moduleclass.module.nameModule,
                'idClass': moduleclass.idClass.idClass
            }
            schedule_data = []
            for schedule in list_schedule:
                schedule_data1 = {
                    'classroom': schedule.class_room.nameClassRoom,
                    'period_start': schedule.period_start,
                    'days_of_week': schedule.days_of_week,
                    'start_date': schedule.start_date,
                    'end_date': schedule.end_date
                }
                schedule_data.append(schedule_data1)
            schedule_exam_data = {
                'classroom': schedule_exam.class_room.nameClassRoom,
                'period': schedule_exam.period_start,
                'date_exam': schedule_exam.date_exam.strftime('%d/%m/%Y'),
            }

            data_1 = {
                'moduleclass' : moduleclass_data,
                'schedule': schedule_data,
                'schedule_exam': schedule_exam_data
            }

            data.append(data_1)
        return JsonResponse({'schedules':data})
    except Student_ModuleClass.DoesNotExist:
        return JsonResponse({'error': 'Sinh viên này không có lớp học phần nào trong kỳ này'})