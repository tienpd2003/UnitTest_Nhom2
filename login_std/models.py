# Create your models here.
from django.db import models
from faculty.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.signals import pre_save
from django.dispatch import receiver


class profile_std(models.Model):
    idStd = models.CharField(max_length=10, verbose_name='MSSV', primary_key=True)
    password = models.CharField(max_length= 128, verbose_name='Mật khẩu')
    nameStd = models.CharField(max_length=32, verbose_name='Họ và tên')
    datebirthStd = models.DateField(verbose_name='Ngày sinh')
    genderStd = models.CharField(max_length=5, choices=[('Nam','Nam'), ('Nữ','Nữ') , ('Khác', 'Khác')], verbose_name='Giới tính')
    identityStd = models.CharField(max_length=15,verbose_name='CCCD/CMND', blank = True, null=True)
    ethnicityStd = models.CharField(max_length=10, default='Kinh', verbose_name='Dân tộc')
    phoneStd = models.CharField(max_length=12, verbose_name='Điện thoại', blank=True, null=True)
    emailStd = models.CharField(max_length=40, verbose_name='Email', blank=True, null=True)
    addressStd = models.CharField(max_length=100, verbose_name='Quê quán')
    idClass = models.ForeignKey(FacultyClasses, on_delete= models.PROTECT, verbose_name='Lớp')
    graduate = models.BooleanField(default=True, choices=[(True, 'Chưa tốt nghiêp'), (False, 'Đã tốt nghiệp')], verbose_name='Tình trạng tốt nghiệp')
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.idStd} - {self.nameStd}'
    
    def is_authenticated(self):
        return True
    
    def set_custom_password(self, raw_password):
        hashed_password = make_password(raw_password)
        self.password = hashed_password

    def check_custom_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        verbose_name = 'Thông tin sinh viên'
        verbose_name_plural = 'Sinh viên'


    # Mã hóa mật khẩu trước khi lưu
@receiver(pre_save, sender = profile_std)
def pre_save_profile_std(sender, instance, **kwargs):
    if instance._state.adding:
        instance.password = make_password(instance.password)