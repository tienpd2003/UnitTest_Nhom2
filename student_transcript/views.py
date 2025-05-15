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


#load page transcript
@login_required(login_url='login_std')
def transcript_view(request):

    getidStd = request.user.idStd
    std_info = profile_std.objects.get(idStd=getidStd)
    stdinfo = {'stdinfo': std_info}

    return render(request, 'transcript.html', stdinfo)



#lay danh sach ky cua sinh vien
@login_required(login_url='login_std')
def get_semester_std(request, idStd):
    try:
        std = profile_std.objects.get(idStd=idStd)
        transcripts = Student_ModuleClass.objects.filter(idStd = std)
        id_moduleclasses = transcripts.values_list('module_class', flat= True).distinct()
        moduleclasses = ModuleClass.objects.filter(idModuleClass__in = id_moduleclasses)
        id_semester = moduleclasses.values_list('semester', flat= True).distinct()
        semesters = Semester.objects.filter(idSemester__in = id_semester)
        data_semesters = []
        for semester in semesters:
            data_semester = {
                'idSemester': semester.idSemester,
                'nameSemester': semester.nameSemester,
            }
            data_semesters.append(data_semester)
        return JsonResponse({'semesters': data_semesters}) 
    except (Student_ModuleClass.DoesNotExist, ModuleClass.DoesNotExist, Semester.DoesNotExist) as e:
        return JsonResponse({'error': "Sinh viên này không có học kỳ nào trong CSDL"})
    

#lay bang diem theo ky
@login_required(login_url='login_admin')
def get_transcript_semester(request, idStd, semester):
    std = profile_std.objects.get(idStd=idStd)
    if semester == 'all':
        transcripts = transcript_all(idStd)
        overall = calculate_overall_grade_all(transcripts)
        return JsonResponse({'transcripts': transcripts, 'overall': overall}) 

    try:
        this_semester = Semester.objects.get(idSemester = semester)
        transcripts = Student_ModuleClass.objects.filter(idStd = std , module_class__semester = this_semester)
        if not transcripts.exists():
            raise Student_ModuleClass.DoesNotExist
        transcript_semester = query_to_json_transcript(transcripts)
        overall_semester = calculate_overall_grade_semester(transcript_semester)
        return JsonResponse({'transcripts': transcript_semester, 'overall': overall_semester})
    except Student_ModuleClass.DoesNotExist:
        return JsonResponse({'error':"Không tìm thấy dữ liệu bảng điểm trong CSDL"})  







#tat ca hoc phan trong tat ca cac ky
def transcript_all(idStd):
    std = profile_std.objects.get(idStd=idStd)
    list_semester = get_list_semester_of_student(std)
    transcript_dict = []
    for semester in list_semester:
        list_transcript = get_list_transcript_by_idstd_semster(std, semester)
        transcript_semester ={
            'semester': semester.nameSemester,
            'transcripts': list_transcript
        }
        transcript_dict.append(transcript_semester)
    
    return transcript_dict
        

    #lay danh sach ky cua sinh vien
def get_list_semester_of_student(student_object):
    list_transcripts = Student_ModuleClass.objects.filter(idStd = student_object)
    id_moduleclasses = list_transcripts.values_list('module_class', flat= True).distinct()
    moduleclasses = ModuleClass.objects.filter(idModuleClass__in = id_moduleclasses)
    id_semester = moduleclasses.values_list('semester', flat= True).distinct()
    semesters = Semester.objects.filter(idSemester__in = id_semester)
    return semesters

    #lay danh sach học phan sinh vien theo ky
def get_list_transcript_by_idstd_semster(student_object, semester_object):
    list_transcripts = Student_ModuleClass.objects.filter(idStd = student_object, module_class__semester = semester_object)
    return query_to_json_transcript(list_transcripts)


#chuyen query sang json transcripts
def query_to_json_transcript(transcripts):
    transcript_data = []
    for transcript in transcripts:
            data_transcript = {
                'idModule': transcript.module_class.module.idModule,
                'nameModule': transcript.module_class.module.nameModule,
                'credit': transcript.module_class.module.credits,
                'moduleclass': transcript.module_class.idClass.idClass,
                'process_grade': transcript.process_grade,
                'final_grade': transcript.final_grade,
                'overall_grade': transcript.overall_grade,
                'overall_grade_4': transcript.overall_grade_4,
                'overall_grade_text': transcript.overall_grade_text,
                'is_pass': 'Đạt' if transcript.is_pass else ('Không đạt' if transcript.is_pass is False else "")
            }
            transcript_data.append(data_transcript)
    return transcript_data



#tinh mot ky
def calculate_overall_grade_semester(transcripts):
    sum_semester_10 = 0
    sum_semester_4 = 0
    credits_pass = 0
    all_credits = 0
    owe_credits = 0
    for transcript in transcripts:
        if transcript['is_pass'] == "Đạt":
            sum_semester_10 = sum_semester_10 + transcript['overall_grade']*transcript['credit']
            sum_semester_4 = sum_semester_4 + transcript['overall_grade_4']*transcript['credit']
            credits_pass = credits_pass + transcript['credit']
            all_credits = all_credits + transcript['credit']
        elif transcript['is_pass'] == "Không đạt":
            all_credits = all_credits + transcript['credit']
            owe_credits = owe_credits + transcript['credit']
        else:
            all_credits = all_credits + transcript['credit']
            continue
    average_semester_10 = sum_semester_10 / credits_pass
    average_semester_4 = sum_semester_4 / credits_pass
    overall_semester = {
        'credits_pass': credits_pass,
        'all_credits': all_credits,
        'average_10': round(average_semester_10,2),
        'average_4': round(average_semester_4,2),
        'owe_credits': owe_credits,
    }
    return overall_semester




#tinnh theo tat ca cac ky
def calculate_overall_grade_all(transcripts_all):
    transcript_all = []
    collect_all_10 = 0
    collect_all_4 = 0
    all_credits = 0
    collect_credits = 0
    owe_credits = 0
    count_semester = 0
    for transcript_semester in transcripts_all:
        count_semester = count_semester + 1
        nameSemester = transcript_semester['semester']
        transcripts = transcript_semester['transcripts']
        overall_semester = calculate_overall_grade_semester(transcripts)
        if overall_semester is not None:
            collect_all_10 = collect_all_10 + overall_semester['average_10']
            collect_all_4 = collect_all_4 + overall_semester['average_4']
            all_credits = all_credits + overall_semester['all_credits']
            collect_credits = collect_credits + overall_semester['credits_pass']
            owe_credits = overall_semester['owe_credits']
            collect_10 = collect_all_10 / count_semester
            collect_4 = collect_all_4 / count_semester

            final_overall_semester = {
                'average_semester_10': overall_semester['average_10'],
                'average_semester_4' : overall_semester['average_4'],
                'average_10' : round(collect_10,2),
                'average_4' : round(collect_4,2),
                'all_credits': all_credits,
                'collected_credits': collect_credits,                       #tat cả
                'passed_credits': overall_semester['credits_pass'],                          #hoc ky
                'owe_credits': owe_credits                               #tin chi no trong ky
            }

            semester_overall = {
                'smester': nameSemester,
                'overall': final_overall_semester
            }

            transcript_all.append(semester_overall)
    return transcript_all
        


            