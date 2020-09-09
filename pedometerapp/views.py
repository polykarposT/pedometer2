from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers
import datetime
from .forms import StepsForm, SearchForm
from .models import Steps

# Create your views here.


def index(request):
    return render(request, 'pedometerapp/index.html')


@login_required
def logout_request(request):
    logout(request)
    return redirect("/")

def login_request(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Invalid username or password.")
        else:
            messages.info(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render (request, 'pedometerapp/login.html', {'form': form})

@login_required
def stats(request):
    steps_records = Steps.objects.all().filter(user=request.user).order_by('-id')[:5]
    current_date = datetime.date.today()
    dates = Steps.objects.all().filter(user=request.user).filter(created_at__exact=current_date)
    context = {'steps_records': steps_records, 'dates': dates,}
    return render(request, 'pedometerapp/stats.html',context)

@login_required
def create_activity(request):
    if request.user.is_authenticated:
        user = request.user

    if request.method == "POST":
        form = StepsForm(request.POST)
        if form.is_valid():
            steps = int(request.POST['steps'])
            date = request.POST['created_at']
            new_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if steps > 50000:
                messages.error(request, 'Please your activity must be between 1 - 50000')
                return redirect('create_activity')
            elif steps < 1:
                messages.error(request, 'Please your activity must be between 1 - 50000')
                return redirect('create_activity')
            check_date = Steps.objects.all().filter(user=request.user).filter(created_at__exact=new_date)
            if check_date:
                messages.error(request, 'You already have activity this date.')
                return redirect('create_activity')
            activity = Steps(user=user, steps=steps, created_at=new_date)
            activity.save()
            return redirect('stats')
    else:
        form = StepsForm()
        current_date = datetime.date.today()
        dates = Steps.objects.all().filter(user=request.user).filter(created_at__exact=current_date)
        context = {'form': form, 'dates':dates}
    return render(request, 'pedometerapp/create_activity.html',context)

def search(request):
    if request.user.is_authenticated:
        user = request.user
    if request.method == 'POST':
        form = SearchForm(request.POST)
        date_from = request.POST['date_from']
        date_to = request.POST['date_to']
        new_date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
        new_date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
        if form.is_valid():
            if new_date_from is None or new_date_to is None or new_date_from and new_date_to is None:
                messages.error(request, 'Your dates can\'t be empty')
                return redirect('search')
            
            data = Steps.objects.all().filter(user=request.user).filter(created_at__range=(new_date_from, new_date_to))
            if data.count() == 0:
                messages.error(request, 'Not even AI could find data in those dates. Please try again.')
                return redirect('search')
            context = {'data': data}
            return render(request, 'pedometerapp/results.html', context)
    else:
        form = SearchForm()
        context = {'form': form}
    return render(request, 'pedometerapp/search.html', context)


def test(request):
    return render(request, 'pedometerapp/test.html',)

def processSearch(request):
    activity_data = []
    dataset = Steps.objects.all().filter(user=request.user).order_by('-created_at')[:5]
    for i in dataset:
        activity_data.append({datetime.datetime.strftime(i.created_at, "%Y-%m-%d"):i.steps})   
    
    return JsonResponse(activity_data, safe=False)

#new search with response for charts
def processSearch2(request):
    date_from = request.GET['date_from']
    date_to = request.GET['date_to']
    new_date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
    new_date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
    if new_date_from is None or new_date_to is None or new_date_from and new_date_to is None:
        messages.error(request, 'Your dates can\'t be empty')
        return redirect('search2')
    
    data = Steps.objects.all().filter(user=request.user).filter(created_at__range=(new_date_from, new_date_to))
    if data.count() == 0:
        messages.error(request, 'Not even AI could find data in those dates. Please try again.')
    activity_data = []
    for i in data:
        activity_data.append({datetime.datetime.strftime(i.created_at, "%Y-%m-%d"): i.steps})

    return JsonResponse(activity_data, safe=False)
