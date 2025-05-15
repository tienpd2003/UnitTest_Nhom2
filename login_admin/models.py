
from django.db import models
from faculty.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.

class profile_admin(models.Model):
    idAdmin = models.CharField(max_length=10, verbose_name='Tên đăng nhập', primary_key=True)
    password = models.CharField(max_length= 128, verbose_name='Mật khẩu')
    nameAdmin = models.CharField(max_length=32, verbose_name='Họ và tên')
    datebirthAdmin = models.DateField(verbose_name='Ngày sinh')
    genderAdmin = models.CharField(max_length=5, choices=[('Nam','Nam'), ('Nữ','Nữ')], verbose_name='Giới tính')
    phoneAdmin = models.CharField(max_length=12, verbose_name='Điện thoại', blank=True, null=True)
    emailAdmin = models.CharField(max_length=40, verbose_name='Email', blank=True, null=True)
    addressAdmin = models.CharField(max_length=50, verbose_name='Quê quán')
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.idAdmin} - {self.nameAdmin}'
    
    def is_authenticated(self):
        return True
    
        
    def set_custom_password(self, raw_password):
        hashed_password = make_password(raw_password)
        self.password = hashed_password

    def check_custom_password(self, raw_password):
        return check_password(raw_password, self.password)


    class Meta:
        verbose_name = 'Quản trị viên'
        verbose_name_plural = 'Quản trị viên'

@receiver(pre_save, sender = profile_admin)
def pre_save_profile_admin(sender, instance, **kwargs):
    if instance._state.adding:
        instance.password = make_password(instance.password)