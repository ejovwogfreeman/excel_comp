import csv, io
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import * 
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
def home_page(request):
    return render(request, 'pages/home.html')

def about_page(request):
    return render(request, 'pages/about.html')

def documentation_page(request):
    return render(request, 'pages/documentation.html')

def contact_page(request):
    return render(request, 'pages/contact.html')

@login_required(login_url="login_page")
def view_csv_page(request):
    context = {
        "csv": Student_csv.objects.all()
    }
    return render(request, 'pages/view_csv.html', context)

@login_required(login_url="login_page")
def profile_page(request):
    return render(request, 'pages/profile.html')

@login_required(login_url="login_page")
def update_profile_page(request):
    if request.method=="POST":
        form = UserUpdateForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            user = form.save()
            # messages.success(request, f'accouunt updated for {user.username} succefully')
            print(f'accouunt updated for {user.username} succefully')
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
            # messages.success(request, f'accouunt created for {user.username} succefully')
            print(f'accouunt created for {user.username} succefully')
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
            # messages.success(request, f'{user.username} logged in successfully')
            print(f'{user.username} logged in successfully')
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
    return redirect('login_page')

@login_required(login_url="login_page")
def compare_csv_page(request):
    return render(request, 'pages/compare_csv.html')

@login_required(login_url="login_page")
def upload_csv_page(request):
    if request.method == "POST":
        csv_file = request.FILES["file"]
        # if not csv_file.name.endswith('.csv') or not csv_file.name.endswith('.xlsx'): 
        #     messages.error(request, 'Invalid file format.')
        if csv_file.name.endswith('.csv') or csv_file.name.endswith('.xlsx'):
            data_set = csv_file.read().decode('UTF-8')
            io_strig = io.StringIO(data_set)
            next(io_strig)
            for column in csv.reader(io_strig, delimiter=',', quotechar="|"):
                _, created = Student_csv.objects.update_or_create(
                    first_name=column[0],
                    last_name=column[1],
                    email=column[2],
                    phone_number = column[3],
                    track = column[4]
                )
            File.objects.create(file=csv_file)
            messages.success(request, 'File uploaded successfully.')
            return redirect('view_csv_page')
        else:
            messages.error(request, 'Invalid file format.')
    return render(request, 'pages/upload_csv.html')


@login_required(login_url="login_page")
def download_csv_page(request):

    items = Student_csv.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="student.csv"'

    writer = csv.writer(response, delimiter=',')
    writer.writerow(['first_name','last_name', 'email', 'phone_number', 'track'])

    for x in items:
        writer.writerow([x.first_name, x.last_name, x.email, x.phone_number, x.track])

    return response


def notfound_page(request, exception):
    return render(request, 'pages/notfound_page.html')
