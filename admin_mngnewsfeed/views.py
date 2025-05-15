from django.shortcuts import render
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
from login_admin.models import profile_admin
import pandas as pd
from PyPDF2 import PdfReader
from newsfeed.models import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files.base import ContentFile





# Create your views here.
@login_required(login_url='login_admin')
def admin_mngnewsfeed(request):

    getidAdmin = request.user.idAdmin                                           # thong tin admin
    admininfo = profile_admin.objects.get(idAdmin=getidAdmin)
    infoAdmin = {'admininfo': admininfo,}

    return render(request, 'admin_mngnewsfeed.html', infoAdmin)


#them moi tin tuc
@login_required(login_url='login_admin')
def save_newsfeed(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        title = request.POST.get('title','')
        pdf_file = request.FILES.get('pdf_file', None).read()
        stt_hidden = request.POST.get('stt_hidden','')
        if title and pdf_file and stt_hidden:
            new_newsfeed = newsfeed(
                title = title,
                pdf_file = pdf_file,
                is_hidden = stt_hidden
            )
            new_newsfeed.save()
            response_data = {'message': 'Thêm mới tin tức thành công'}
            return JsonResponse(response_data)
        else:
            response_data = {'message': 'Hãy nhập đủ các trường'}
            return JsonResponse(response_data)
    

#tim kiem tin tuc
@login_required(login_url='login_admin')
def get_newsfeed(request, search_value):
    response_data = []
    if search_value == 'all':
        list_newsfeed = newsfeed.objects.all()
        for newsfeed1 in list_newsfeed:
            newsfeed_data = {
                'id': newsfeed1.id,
                'post_date': newsfeed1.post_date.strftime('%d/%m/%Y'),
                'title': newsfeed1.title,
                'is_hidden': 'Hiển thị' if newsfeed1.is_hidden else 'Ẩn'
            }
            response_data.append(newsfeed_data)
        return JsonResponse({'newsfeeds': response_data})
    else:
        list_newsfeed = newsfeed.objects.filter(
            Q(post_date__icontains=search_value) |
            Q(title__icontains=search_value)
            )
        for newsfeed1 in list_newsfeed:
            newsfeed_data = {
                'post_date': newsfeed1.post_date,
                'title': newsfeed1.title,
                'is_hidden': 'Hiển thị' if newsfeed1.is_hidden else 'Ẩn'
            }
            response_data.append(newsfeed_data)
        return JsonResponse({'newsfeeds': response_data})
    


@login_required(login_url='login_admin')
def delete_newsfeed(request, idnf):
    try:
        nf = newsfeed.objects.get(id = idnf)
        nf.delete()
        return JsonResponse({"message": "Xóa tin thành công"})
    except newsfeed.DoesNotExist:
        return JsonResponse({"message": "Tin không tồn tại"})
