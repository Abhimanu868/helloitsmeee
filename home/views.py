from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from home.models import Contact
from django.core.mail import send_mail
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')

@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        des = request.POST.get('description')
        contact = Contact(name=name, email=email, phone=phone, des=des)
        contact.save()
    return render(request, 'contact.html')

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpass = request.POST.get('confirm_password')
        if password != confirmpass:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.save()
        return redirect('home')
    else:
        return render(request, 'signup.html')
@login_required(login_url='login')
def logoutuser(request):
    logout(request)
    return redirect('login')