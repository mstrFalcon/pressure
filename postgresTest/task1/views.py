import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import formats
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pressure

from django.db.models import Func, F, Value, Avg


def index(request):
    if request.method == "POST":
        pressureSystolic = int(request.POST.get("inputSystolic"))
        pressureDiastolic = int(request.POST.get("inputDiastolic"))
        checkbox = request.POST.getlist("is_defaultdate") # list
        d = request.POST.get("date_input")
        if checkbox:
            d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S%z")
        x = Pressure.objects.create(systolic=pressureSystolic, diastolic=pressureDiastolic, date=d)
        x.save()
        return redirect("index")
    context = {"pressure": Pressure.objects.order_by('date').reverse()[0:5]}
    return render(request, "task1/index.html", context)

def statistics(request):
    return render(request, "task1/statistics.html")

class ChartData(APIView):
    #authentication_classes = []
    #permission_classes = []

    def get(self, request, format=None):
        labels = Pressure.objects.only('date').order_by('date')
        date_format = '%Y-%m-%d %H:%M:%S%z'
        labelsNew = [''] * labels.count()
        for i in range(labels.count()):
            labelsNew[i] = datetime.datetime.strptime(str(labels[i].date), date_format).strftime('%d-%m-%Y %H:%M')
        chartdata1 = Pressure.objects.values_list('systolic').order_by('date')
        chartdata2 = Pressure.objects.values_list('diastolic').order_by('date')
        chartLabel1 = "Верхнее (систолическое) давление"
        chartLabel2 = "Нижнее (диастолическое) давление"
        data = {
            "labelsDate": labelsNew,
            "chartLabel1": chartLabel1,
            "chartLabel2": chartLabel2,
            "chartDataSystolic": chartdata1,
            "chartDataDiastolic": chartdata2,
        }
        return Response(data)

    def post(self, request, format=None):
        dateInputStartString = request.data.get("dateInputStart")
        dateInputEndString = request.data.get("dateInputEnd")
        dateInputStart = datetime.datetime.strptime(dateInputStartString, '%Y-%m-%dT%H:%M')
        dateInputEnd = datetime.datetime.strptime(dateInputEndString, '%Y-%m-%dT%H:%M')
        timeInterval = request.data.get("timeInterval")

        chartLabel1 = "Верхнее (систолическое) давление"
        chartLabel2 = "Нижнее (диастолическое) давление"
        checkbox = request.data.get("checkBoxHide")
        checkbox = checkbox == "true"

        if timeInterval == "day":
            chartdata1 = Pressure.objects.values_list('systolic').order_by('date')
            chartdata2 = Pressure.objects.values_list('diastolic').order_by('date')
            labels = Pressure.objects.only('date').order_by('date')
            if checkbox is True:
                chartdata1 = Pressure.objects.values_list('systolic').filter(date__range=[dateInputStart, dateInputEnd]).order_by('date')
                chartdata2 = Pressure.objects.values_list('diastolic').filter(date__range=[dateInputStart, dateInputEnd]).order_by('date')
                labels = Pressure.objects.only('date').order_by('date').filter(date__range=[dateInputStart, dateInputEnd])
            date_format = '%Y-%m-%d %H:%M:%S%z'
            labelsNew = [''] * labels.count()
            for i in range(labels.count()):
                labelsNew[i] = datetime.datetime.strptime(str(labels[i].date), date_format).strftime('%d-%m-%Y %H:%M')
            data = {
                "labelsDate": labelsNew,
                "chartLabel1": chartLabel1,
                "chartLabel2": chartLabel2,
                "chartDataSystolic": chartdata1,
                "chartDataDiastolic": chartdata2,
            }
            return Response(data)

        if timeInterval == "month":
            labels = Pressure.objects.values('date__month', 'date__year').annotate(systolic=Avg('systolic'), diastolic=Avg('diastolic')).order_by('date__year', 'date__month')
            if checkbox is True:
                labels = (Pressure.objects.values('date__month', 'date__year').annotate(systolic=Avg('systolic'), diastolic=Avg('diastolic')).
                          order_by('date__year', 'date__month').
                          filter(date__range=[dateInputStart, dateInputEnd]))
            labelsNew = [''] * labels.count()
            for i in range(labels.count()):
                labelsNew[i] = ("0" if labels[i]['date__month'] < 10 else "") + str(labels[i]['date__month']) + "-" + str(labels[i]['date__year'])
            chartdata1 = [labels[i]['systolic'] for i in range(len(labels))]
            chartdata2 = [labels[i]['diastolic'] for i in range(len(labels))]
            data = {
                "labelsDate": labelsNew,
                "chartLabel1": chartLabel1,
                "chartLabel2": chartLabel2,
                "chartDataSystolic": chartdata1,
                "chartDataDiastolic": chartdata2,
            }
            return Response(data)

        if timeInterval == "year":
            labels = Pressure.objects.values('date__year').annotate(systolic=Avg('systolic'), diastolic=Avg('diastolic')).order_by('date__year')
            if checkbox is True:
                labels = (Pressure.objects.values('date__year').annotate(systolic=Avg('systolic'), diastolic=Avg('diastolic')).
                          order_by('date__year').
                          filter(date__range=[dateInputStart, dateInputEnd]))
            labelsNew = [''] * labels.count()
            for i in range(labels.count()):
                labelsNew[i] = str(labels[i]['date__year'])
            chartdata1 = [labels[i]['systolic'] for i in range(len(labels))]
            chartdata2 = [labels[i]['diastolic'] for i in range(len(labels))]
            data = {
                "labelsDate": labelsNew,
                "chartLabel1": chartLabel1,
                "chartLabel2": chartLabel2,
                "chartDataSystolic": chartdata1,
                "chartDataDiastolic": chartdata2,
            }
            return Response(data)
        return Response()
