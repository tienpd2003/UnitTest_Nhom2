from django.db import models
from course.models import *

#table phòng học
class ClassRoom(models.Model):
    idClassRoom = models.CharField(max_length=10, primary_key= True, verbose_name='Mã phòng học')
    nameClassRoom = models.CharField(max_length=20, verbose_name= "Tên phòng học")

    def __str__(self):
        return self.idClassRoom
    class Meta:
        verbose_name = 'Phòng học'
        verbose_name_plural = 'Danh sách phòng học'

#table lịch học cho lớp học phần
class ScheduleModuleClass(models.Model):
    days_of_week = [                                                             #thu trong tuan
        ('T2','T2'),
        ('T3','T3'),
        ('T4','T4'),
        ('T5','T5'),
        ('T6','T6'),
        ('T7','T7'),
        ('CN','CN'),
    ]
    period_start = [                                                            #tiet bat dau
        ('1','1') , ('4','4'), ('7','7'), ('10','10'), ('13','13')
    ]

    idSMC = models.AutoField(primary_key=True)
    idModuleClass = models.ForeignKey(ModuleClass, on_delete=models.CASCADE, related_name='schedules', verbose_name='Lớp học phần')
    days_of_week = models.CharField(max_length=2, choices=days_of_week, verbose_name='Thứ')
    period_start = models.CharField(max_length=2, choices=period_start, verbose_name='Tiết bắt đầu')
    periods_count = models.IntegerField(default= 3, verbose_name='Số tiết')
    start_date = models.DateField(verbose_name= 'Ngày bắt đầu', null= True, blank= True)
    end_date = models.DateField(verbose_name= 'Ngày kết thúc', null= True, blank= True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, verbose_name= 'Phòng học', null = True, blank= True)

    class Meta:
        verbose_name = 'Lịch học'
        verbose_name_plural = 'Lịch học'


#table lịch thi

class ScheduleFinalExam(models.Model):
    period_start = [                                                            #tiet bat dau
        ('1','1') , ('4','4'), ('7','7'), ('10','10'), ('13','13')
    ]
    idSFE = models.AutoField(primary_key=True)
    idModuleClass = models.ForeignKey(ModuleClass, on_delete=models.CASCADE, related_name='finalexam', verbose_name='Lớp học phần')
    date_exam = models.DateField(verbose_name= 'Ngày thi', null= True, blank= True)    
    period_start = models.CharField(max_length=2, choices=period_start, verbose_name='Tiết bắt đầu')
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, verbose_name= 'Phòng học', null = True, blank= True)

    class Meta:
        verbose_name = 'Lịch thi'
        verbose_name_plural = 'Lịch thi'



