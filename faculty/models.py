from django.db import models

# bảng danh sách các khoa
class Faculty(models.Model):
    idFaculty = models.CharField(max_length=10, verbose_name= "Mã khoa", primary_key= True)
    nameFaculty = models.CharField(max_length=50, verbose_name= "Tên khoa")

    def __str__(self):
        return self.nameFaculty
    
    class Meta:
        verbose_name = "Khoa"
        verbose_name_plural = "Khoa"



#bảng danh sách các ngành trong một khoa
class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete= models.CASCADE, verbose_name= "Tên Khoa" )
    idDepartment = models.CharField(max_length=10, verbose_name= "Mã ngành", primary_key= True )
    nameDepartment = models.CharField(max_length=50, verbose_name= "Tên Ngành")

    def __str__(self):
        return self.nameDepartment
    
    class Meta:
        verbose_name = "Ngành đào tạo"
        verbose_name_plural = "Ngành đào tạo"


class idCourse(models.Model):
    idCourse = models.CharField(max_length=3, verbose_name= "Mã khóa", primary_key= True)
    nameCourse = models.CharField(max_length=20, verbose_name="Tên khóa")
    
    def __str__(self):
        return self.nameCourse
    
    class Meta:
        verbose_name = "Khóa sinh viên"
        verbose_name_plural = "Khóa sinh viên"



# bảng danh sách lớp thuộc khoa
class FacultyClasses(models.Model):
    idClass = models.CharField(max_length = 10, verbose_name= "Mã lớp", primary_key= True)
    department = models.ForeignKey(Department, on_delete= models.CASCADE, related_name="department_class",verbose_name= "Tên Ngành")
    idCourse = models.ForeignKey(idCourse, on_delete = models.CASCADE, verbose_name = "Khóa")

    def __str__(self):
        return self.idClass

    class Meta:
        verbose_name = "Lớp"
        verbose_name_plural = "Lớp"