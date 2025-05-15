from django.db import models
from login_std.models import *
from course.models import *

# Create your models here.
class tuitionfee(models.Model):
    id =  models.AutoField(primary_key=True),
    idStd = models.ForeignKey(profile_std, on_delete=models.CASCADE, verbose_name= 'Mã sinh viên')
    idSemester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name= 'Học kỳ', related_name="semester_tuitionfee")
    totalcredit = models.IntegerField(verbose_name= 'Tín chỉ đăng ký')
    total_tuitionfee = models.CharField(max_length= 20, verbose_name= 'Học phí')
    paid_tuitionfee = models.CharField(max_length= 20, verbose_name= 'Đã đóng')
    unpaid_tuitionfee = models.CharField(max_length= 20, verbose_name= 'Còn nợ')

    class Meta:
        verbose_name = 'Học phí'
        verbose_name_plural = 'Học phí'
    

class tuitionfee_scale(models.Model):
    id =  models.AutoField(primary_key=True),
    idSemester = models.OneToOneField(Semester, on_delete=models.CASCADE, verbose_name= 'Học kỳ')
    scale = models.FloatField(verbose_name="Học phí tín chỉ")

    class Meta:
        verbose_name = 'Giá tín chỉ'
        verbose_name_plural = 'Giá tín chỉ'
    