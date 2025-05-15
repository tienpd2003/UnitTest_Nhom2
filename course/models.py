from django.db import models
from login_std.models import profile_std
from faculty.models import *

#bang hoc ky
class Semester(models.Model):
    idSemester = models.CharField(max_length= 10, verbose_name= 'Mã học kỳ', primary_key= True)
    nameSemester = models.CharField(max_length= 30, verbose_name= 'Học kỳ')
    start_date = models.DateField(verbose_name= 'Ngày bắt đầu')
    end_date = models.DateField(verbose_name= 'Ngày kết thúc')
    
    def __str__(self):
        return f"{self.idSemester} - {self.nameSemester}"

    class Meta:
        verbose_name = 'Học kỳ'
        verbose_name_plural = 'Học kỳ'


#bang mon hoc
class Module(models.Model):
    idModule = models.CharField(max_length=10, verbose_name='Mã học phần', primary_key= True)
    nameModule = models.CharField(max_length=70, verbose_name='Tên học phần')
    credits = models.IntegerField(default=0, verbose_name='Số tín chỉ')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name= 'Chuyên ngành', related_name='Module_of_Department')
    process_ratio = models.FloatField(verbose_name='Hệ số điểm quá trình', blank = True, null = True, default= 0.3)
    final_ratio = models.FloatField(verbose_name='Hệ số điểm kết thúc', blank = True, null = True, default=0.7)
    

    def __str__(self):
        return f"{self.idModule} - {self.nameModule}"
    
    class Meta:
        verbose_name = 'Học phần'
        verbose_name_plural = 'Danh sách học phần'


#bang lop hoc phan
class ModuleClass(models.Model):
    idModuleClass = models.AutoField(primary_key=True, verbose_name="Mã lớp học phần")
    module = models.ForeignKey(Module, on_delete= models.CASCADE, related_name="ModuleClass_module", verbose_name= "Tên học phần")
    idClass = models.ForeignKey(FacultyClasses, on_delete = models.CASCADE, verbose_name= 'Lớp học phần', related_name='Module_of_idClass')
    semester = models.ForeignKey(Semester, on_delete= models.CASCADE, verbose_name= 'Học kỳ')
    max_slot = models.PositiveIntegerField(verbose_name="Sĩ số tối đa")
    def __str__(self):
        return f'{self.idClass.idClass}_{self.module.idModule}_{self.module.nameModule}'
    
    class Meta:
        verbose_name = 'Lớp học phần'
        verbose_name_plural = 'Lớp học phần'




#bang luu mon hoc da dang ky cho sinh vien + bảng điểm
class Student_ModuleClass(models.Model):
    id = models.AutoField(primary_key=True)
    module_class = models.ForeignKey(ModuleClass, on_delete= models.CASCADE, related_name= 'module_std' ,verbose_name='Học phần')
    idStd = models.ForeignKey(profile_std, on_delete= models.CASCADE, related_name='std_module', verbose_name='MSSV')
    process_grade = models.FloatField(verbose_name='Điểm quá trình', blank = True, null = True)
    final_grade = models.FloatField(verbose_name='Điểm kết thúc', blank = True, null = True)
    overall_grade = models.FloatField(verbose_name='Điểm tổng kết', blank = True, null = True)
    overall_grade_4 = models.FloatField(verbose_name='Hệ số 4', blank = True, null = True)
    overall_grade_text = models.CharField(max_length=2, verbose_name='Điểm chữ', blank = True, null = True)
    is_pass = models.BooleanField(choices=[(True, 'Đạt'), (False, 'Chưa đạt')], blank = True, null = True, verbose_name='Đạt')

    def __str__(self):
        return f'{self.idStd.idStd} - {self.module_class.module.nameModule}'


    def calculate_grade(self):
        process_ratio = self.module_class.module.process_ratio
        final_ratio = self.module_class.module.final_ratio
        if self.process_grade is not None and self.final_grade is not None:
            self.overall_grade = round(self.process_grade*process_ratio + self.final_grade*final_ratio,2)
            
            if self.overall_grade >= 8.5:
                self.overall_grade_4 = 4.0
                self.overall_grade_text = 'A'
                self.is_pass = True
            elif self.overall_grade >= 8.0:
                self.overall_grade_4 = 3.5
                self.overall_grade_text = 'B+'
                self.is_pass = True
            elif self.overall_grade >= 7.5:
                self.overall_grade_4 = 3.0
                self.overall_grade_text = 'B'
                self.is_pass = True
            elif self.overall_grade >= 6.5:
                self.overall_grade_4 = 2.5
                self.overall_grade_text = 'C+'
                self.is_pass = True
            elif self.overall_grade >= 6.0:
                self.overall_grade_4 = 2.0
                self.overall_grade_text = 'C'
                self.is_pass = True
            elif self.overall_grade >= 5.0:
                self.overall_grade_4 = 1.5
                self.overall_grade_text = 'D+'
                self.is_pass = True
            elif self.overall_grade >= 4.0:
                self.overall_grade_4 = 1
                self.overall_grade_text = 'D'
                self.is_pass = True
            else:
                self.overall_grade_4 = 0.0
                self.overall_grade_text = 'F'
                self.is_pass = False


    def save_grade(self, *args, **kwargs):
        super().save(*args, **kwargs)

        
    def save(self, *args, **kwargs):
        self.calculate_grade()
        self.save_grade()

    class Meta:
        verbose_name = 'Bảng điểm'
        verbose_name_plural = 'Bảng điểm'


#bang lich dang ky mon hoc
class RegistrationSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester, on_delete= models.CASCADE, verbose_name= "Học kỳ")
    idCourse = models.ForeignKey(idCourse, on_delete= models.CASCADE, verbose_name= "Khóa")
    start_date = models.DateField(verbose_name="Ngày bắt đầu")
    end_date = models.DateField(verbose_name="Ngày kết thúc")
    def __str__(self):
        return self.semester.nameSemester

    class Meta:
        verbose_name = "Lịch đăng ký học phần"
        verbose_name_plural = "Lịch đăng ký học phần"