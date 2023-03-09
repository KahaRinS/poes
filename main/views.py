from django.shortcuts import render
from .models import *
from .forms import RegionForm, SensorForm, ResultForm
from users.forms import CustomUserCreationForm
from django.utils.dateparse import parse_date

def index(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            error = ''
            form.save()
        else:
            pass
    form = RegionForm
    data = {
        'form': form,
        'Results': Results.objects.all(),
    }
    return render(request, 'main/index.html', data)

def RegionView(request):
    error = ''
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            error = ''
            form.save()
        else:
            error = 'plohie dannie'
    form = RegionForm
    data = {
        'form': form,
        'Raw': Region.objects.all(),
        'name': 'Регионы',
        'ern': error,
    }
    return render(request, 'main/region.html', data)

def SensorView(request):
    error = ''
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            error = ''
            form.save()
        else:
            error = 'plohie dannie'
    form = SensorForm
    data = {
        'form': form,
        'Raw': Sensors.objects.all(),
        'name': 'Датчики',
        'ern': error,
    }
    return render(request, 'main/sensor.html', data)

def ResultView(request):
    error = ''
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error = 'plohie dannie'

    form = ResultForm
    data = {
        'form': form,
        'Raw': Results.objects.all(),
        'name': 'Результаты',
        'ern': error,
    }
    return render(request, 'main/result.html', data)

def MainView(request):
    # print(request.POST)
    data = {
        'Raw': Results.objects.order_by('date'),
        'form': SensorForm,
    }
    results = Results.objects.all()

    if '1' in request.POST:
        date = parse_date(request.POST['date'])
        data1 = results.filter(date=date)
        data['first'] = data1

    elif '2' in request.POST:
        datemin = parse_date(request.POST['datemin'])
        datemax = parse_date(request.POST['datemax'])
        date = results.filter(date__range=[datemin, datemax])
        temp = []
        for el in date:
            temp.append(el.temp)
        print(date)
        if data:
            data['max'] = f'Максимальная температура: {max(temp)}'
            data['min'] = f'Минимальная температура: {min(temp)}'

    elif '3' in request.POST:
        sensors = Sensors.objects.all()
        sorted_sensors = sensors.filter(region = request.POST['region'])
        data['sens'] = sorted_sensors

    results = Results.objects.all()
    i = 0
    av_temp = 0
    for el in results:
        i+=1
        av_temp = av_temp + el.temp
    print(i)
    av_temp = av_temp/i
    f = open('text.txt', 'w')
    for el in results:
        f.write(f'{el.date}: {av_temp-el.temp} \n')
    f.close()
    print(av_temp)
    return render(request, 'main/boba.html', data)