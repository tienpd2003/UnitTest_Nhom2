from django.db import models
from datetime import date

# Create your models here.
class newsfeed(models.Model):
    id = models.AutoField(primary_key= True)
    title = models.CharField(max_length=255, verbose_name= "Tiêu đề thông báo")
    pdf_file = models.BinaryField(blank=True, null=True, verbose_name="file_pdf")
    post_date = models.DateField(blank=True, null=True, default=date.today, verbose_name="Ngày đăng")
    is_hidden = models.BooleanField(choices=[(True, 'Hiện'), (False, 'Ẩn')], blank = True, null = True, default= True, verbose_name="Ẩn / hiện")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Tin tức'
        verbose_name_plural = 'Tin tức'