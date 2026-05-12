
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.') # تطبيق Task 5
    return redirect('login') # تحويل المستخدم لصفحة الدخول بعد الخروج


def login_user(request):
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(username=u, password=p)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'login successfully') 
            return redirect('list_students')
        else:
            messages.error(request, 'error message')
            
    return render(request, 'usermodule/login.html')

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered!') 
            return redirect('login') # سنقوم بإنشاء رابط login في الخطوة القادمة
        
    else:
        form = RegisterForm()
    return render(request, 'usermodule/register.html', {'form': form})