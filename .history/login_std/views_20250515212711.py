
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .backends import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import profile_std
from django.test import override_settings
from django.http import JsonResponse

#view login danh cho sinh vien
@override_settings(AUTHENTICATION_BACKENDS=['login_std.backends.CustomAuthBackendStd'])
def login_std(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user_std = authenticate(request, username=username, password=password)
        print(user_std)
        print(1)
        if user_std is not None:
            # if 'session_key' in request.session:
            #     request.session.flush()
            login(request, user_std)
            print(2)
            return redirect('profile')
        else:
            messages.error(request, 'Sai thông tin tài khoản')
    return render(request, 'login_std.html')




# Create your views here.
@login_required(login_url='login_std')
def profile_view(request):
    getidStd = request.user.idStd
   
    stdinfo = profile_std.objects.get(idStd=getidStd)
    datebirth = stdinfo.datebirthStd
    context = {'stdinfo': stdinfo, 'datebirth': datebirth.strftime('%d/%m/%Y')}

    return render(request, 'profile.html', context)



@login_required(login_url='login_std')
def logout_std_view(request):
    logout(request)
    return redirect('login_std')



#change password page
@login_required(login_url='login_std')
def change_password_view(request):
    getidStd = request.user.idStd
   
    stdinfo = profile_std.objects.get(idStd=getidStd)
    context = {'stdinfo': stdinfo}

    return render(request, 'change_password.html', context)


#change password
@login_required(login_url='login_std')
def change_password(request):
    idStd = request.user.idStd
    if request.method == 'POST':
        data_password = json.loads(request.body)
        old_password = data_password.get('old_password')
        new_password = data_password.get('new_password')
        try:
            std = profile_std.objects.get(idStd = idStd)
            is_check = check_password(old_password, std.password)
            if (is_check):
                std.set_custom_password(new_password)
                std.save()
                return JsonResponse({"ok":"ok"})
            else:
                return JsonResponse({"notok":"notok"})
        except:
            pass