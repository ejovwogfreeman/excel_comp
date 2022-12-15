import csv, io, os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import * 
from .models import *
import pandas as pd
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
def home_page(request):
    return render(request, 'pages/home.html')

def documentation_page(request):
    return render(request, 'pages/documentation.html')


@login_required(login_url="login_page")
def view_csv_page(request):
    context = {
        "csv": File.objects.all()
    }
    return render(request, 'pages/view_csv.html', context)

@login_required(login_url="login_page")
def view_csv_detail_page(request, pk):
    csv_file = File.objects.get(id=pk)
    print(csv_file.file.url)
    df = pd.read_csv("http://127.0.0.1:8000/" + csv_file.file.url)
    # print(df)
    context = {
        'df': df.to_html()
    }
    return render(request, 'pages/view_csv_detail.html', context)

@login_required(login_url="login_page")
def profile_page(request):
    csv_file = File.objects.filter(author = request.user)
    context = {
        "csv": csv_file
    }
    return render(request, 'pages/profile.html', context)

@login_required(login_url="login_page")
def update_profile_page(request):
    if request.method=="POST":
        form = UserUpdateForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'accouunt updated for {user.username} succefully')
            return redirect('profile_page')
    else:
        form = UserUpdateForm(instance = request.user)
    context = {
        'form': form
    }
    return render(request, 'pages/profile_update.html', context)

def register_page(request):
    if request.user.is_authenticated:
        return redirect('view_csv_page')
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'accouunt created for {user.username} succefully')
            return redirect('login_page')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'pages/register.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('view_csv_page')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have logged in successfully')
            if 'next' in request.GET:
                return redirect(request.GET.get('next'))
            else:
                return redirect('view_csv_page')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'pages/login.html', context)

def logout_page(request):
    logout(request)
    messages.warning(request, 'You have logged out, log in again to continue')
    return redirect('login_page')

@login_required(login_url="login_page")
def compare_csv_page(request):
    return render(request, 'pages/compare_csv.html')

@login_required(login_url="login_page")
def upload_csv_page(request):
    if request.method == "POST":
        csv_file = request.FILES["file"]
        if csv_file.name.endswith('.csv') or csv_file.name.endswith('.xlsx'):
            File.objects.create(file=csv_file, author=request.user)
            messages.success(request, 'File uploaded successfully.')
            return redirect('view_csv_page')
        else:
            messages.warning(request, 'Invalid file format.')
    return render(request, 'pages/upload_csv.html')


@login_required(login_url="login_page")
def delete_csv_page(request, pk):
    csv_file = File.objects.get(id=pk)
    csv_file.delete()
    messages.warning(request, 'File Deleted successfully.')
    return redirect('view_csv_page')

def notfound_page(request, exception):
    return render(request, 'pages/notfound_page.html')
