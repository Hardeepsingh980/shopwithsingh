from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from shop.models import Product


# @login_required
# def admin(request):
#     return render(request, 'accounts/admin.html')


def signup(request):
    if request.method == 'POST':
        try:
            User.objects.get(username=request.POST['username'])
            return render(request, 'accounts/signup.html',{'error':'Username already exist'})
        except User.DoesNotExist:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            return redirect('home')
            
    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user != None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html',{'error':'Username Or Password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    else:
        auth.logout(request)
        return redirect('home')



def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', context={'products':products})