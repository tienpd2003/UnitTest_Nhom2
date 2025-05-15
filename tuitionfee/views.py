from django.forms import model_to_dict
from django.shortcuts import render
from login_std.models import profile_std
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from course.models import *
from .models import *
from django.http import JsonResponse
# Create your views here.


#load trang hoc phi
@login_required(login_url='login_std')
def tuitionfee_view(request):

    getidStd = request.user.idStd
    std_info = profile_std.objects.get(idStd=getidStd)
    stdinfo = {'stdinfo': std_info}

    return render(request, 'tuitionfee.html', stdinfo)




#lay du lieu ve hoc phi:
@login_required(login_url='login_std')
def get_tuitionfee(request):
    idStd = request.user.idStd
    std = profile_std.objects.get(idStd=idStd)
    semesters = Semester.objects.filter(semester_tuitionfee__idStd = std)
    semester_tuitionfee = []
    for semester in semesters:
        tuitionfee_scale_obj = tuitionfee_scale.objects.get(idSemester = semester)
        tuitionfee_scale_value = int(tuitionfee_scale_obj.scale)
        moduleclass_tuitionfee = get_moduleclass(std, semester)
        this_tuititonfee = tuitionfee.objects.get(idStd = std, idSemester = semester)
        tuitionfee_data = model_to_dict(this_tuititonfee)
        tuitionfee_semester = {
            'semester': semester.nameSemester,
            'moduleclasses': moduleclass_tuitionfee,
            'tuitionfee': tuitionfee_data,
            'idSemester': semester.idSemester,
            'tuitionfee_scale': tuitionfee_scale_value
        }
        semester_tuitionfee.append(tuitionfee_semester)
    return JsonResponse({'semester_tuitionfees':semester_tuitionfee})



def get_moduleclass(std, semester):
    try:
        list_moduleclass = ModuleClass.objects.filter(module_std__idStd = std, semester = semester)
        if  not list_moduleclass.exists():
            raise ModuleClass.DoesNotExist
        list_moduleclass_data = []
        for moduleclass in list_moduleclass:
            idModule = moduleclass.module.idModule
            nameModule = moduleclass.module.nameModule
            credit = moduleclass.module.credits
            idClass = moduleclass.idClass
            moduleclass_data = {
                'idModule': idModule,
                'nameModule': nameModule,
                'credit': credit,
                'idClass': idClass.idClass
            }
            list_moduleclass_data.append(moduleclass_data)
        data =  list_moduleclass_data
    except ModuleClass.DoesNotExist:
        pass
    return data
    












#cap nhat lai tuitionfee khi co thay doi trong student_moduleclass
@receiver(post_save, sender = Student_ModuleClass)
@receiver(post_delete, sender = Student_ModuleClass)
def update_tuitionfee(sender,  instance, **kwargs):
    std = instance.idStd
    try:
        list_moduleclass = ModuleClass.objects.filter(module_std__idStd = std)
        if not list_moduleclass.exists():
            raise ModuleClass.DoesNotExist
        id_semesters = list_moduleclass.values_list('semester', flat=True).distinct()
        semesters = Semester.objects.filter(idSemester__in=id_semesters)
        for semester in semesters:
            try:
                tuitionfee_exists = tuitionfee.objects.filter(idStd = std)
                if (not tuitionfee_exists.exists()) or (len(tuitionfee_exists) <= len(semesters)):
                    raise tuitionfee.DoesNotExist
                for tuitionfee_exist in tuitionfee_exists:
                    check = True
                    semester_tuitionfee = tuitionfee_exist.idSemester
                    if semester_tuitionfee.idSemester == semester.idSemester:
                        check = False
                if check:
                    save_tuitionfee_zero(tuitionfee_exist)
            except tuitionfee.DoesNotExist:
                pass
            credits_semesters = 0
            list_moduleclass_semester = ModuleClass.objects.filter(module_std__idStd = std, semester = semester)
            for module_class_semester in list_moduleclass_semester:
                credits = 0
                module = module_class_semester.module
                credits = module.credits
                credits_semesters += credits
                credits = 0
                save_tuitionfee(std, semester, credits_semesters)
    except ModuleClass.DoesNotExist:
        exist_tuitionfee = tuitionfee.objects.filter(idStd = std)
        if exist_tuitionfee.exists():
            for tuitionfee1 in exist_tuitionfee:
                save_tuitionfee_zero(tuitionfee1)




#ham luu hoc phi
def save_tuitionfee(std, semester, credits_semesters):
    tuitionfee_scale_obj = tuitionfee_scale.objects.get(idSemester=semester)
    tuitionfee_scale_value = int(tuitionfee_scale_obj.scale)

    try:
        tuitionfee_semester = tuitionfee.objects.get(idStd = std, idSemester = semester)
        tuitionfee_semester.totalcredit = credits_semesters
        tuitionfee_semester.total_tuitionfee = credits_semesters * tuitionfee_scale_value
        tuitionfee_semester.unpaid_tuitionfee = credits_semesters * tuitionfee_scale_value - int(tuitionfee_semester.paid_tuitionfee)

        tuitionfee_semester.save()
        
    except tuitionfee.DoesNotExist:
        new_tuitionfee = tuitionfee(
            idStd = std,
            idSemester = semester,
            totalcredit =  credits_semesters,
            total_tuitionfee = credits_semesters * tuitionfee_scale_value,
            paid_tuitionfee = 0,
            unpaid_tuitionfee = credits_semesters * tuitionfee_scale_value
        )
        new_tuitionfee.save()


def save_tuitionfee_zero(tuitionfee_zero):
    tuitionfee_zero.totalcredit = 0
    tuitionfee_zero.total_tuitionfee = 0
    tuitionfee_zero.unpaid_tuitionfee = 0
    tuitionfee_zero.save()




#lay danh sach ky cua sinh vien
@login_required(login_url='login_std')
def get_semester_std(request):
    idStd = request.user.idStd
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