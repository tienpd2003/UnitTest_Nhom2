
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .backends import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.test import override_settings
# Create your views here.



#view login danh cho quan tri vien
@override_settings(AUTHENTICATION_BACKENDS=['login_admin.backends.CustomAuthBackendAdmin'])
def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_admin = authenticate(request,username=username, password=password)
        
        if user_admin is not None:
            if 'session_key' in request.session:
                request.session.flush()

            login(request, user_admin)
            
            return redirect('admin_mngprofilestd')
        else:
            messages.error(request, 'Sai thông tin tài khoản')
    return render(request, 'login_admin.html')




#view dang xuat
@login_required(login_url='login_admin')
def logout_admin_view(request):
    logout(request)
    return redirect('login_admin')



#change password page
@login_required(login_url='login_admin')
def change_password_admin_view(request):
    getidAdmin = request.user.idAdmin
   
    admininfo = profile_admin.objects.get(idAdmin=getidAdmin)
    context = {'admininfo': admininfo}

    return render(request, 'change_password_admin.html', context)


#change password
@login_required(login_url='login_admin')
def change_password_admin(request):
    idAdmin = request.user.idAdmin
    if request.method == 'POST':
        data_password = json.loads(request.body)
        old_password = data_password.get('old_password')
        new_password = data_password.get('new_password')
        try:
            std = profile_admin.objects.get(idAdmin = idAdmin)
            is_check = check_password(old_password, std.password)
            if (is_check):
                std.set_custom_password(new_password)
                std.save()
                return JsonResponse({"ok":"ok"})
            else:
                return JsonResponse({"notok":"notok"})
        except:
            pass


