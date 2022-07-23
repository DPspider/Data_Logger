from multiprocessing import context
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import HttpResponse
from yaml import serialize
from api.serializers import DeviceSerializer, ProgrammableParameterSerializer, ReportSerializer

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import  reverse, path, re_path, include, reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib import auth, messages
from django.core.signing import TimestampSigner



from dashboard.models import ProgrammableParameters, Report, Devices, UserProfile

import requests


@api_view(['GET'])
def getData(request):
    ind_readings = Report.objects.all()
    print("ind_readings ", ind_readings)
    device_data = Devices.objects.filter(id = ind_readings[0].id)
    print("device_data-  ", device_data[0].company_id)

    company_data = UserProfile.objects.filter(username = device_data[0].company_id)
    
    serializer = ReportSerializer(ind_readings, many=True)
    print("Company_data-  ", company_data[0].company_image)
    
    
    context = {
        "device_readings" : ind_readings,
        "device_data" : device_data,
        "company_data" : company_data,

    }
    return render(request, 'report.html', context)


@api_view(['POST'])
def addValues(request):
    serializer_class = ReportSerializer(data=request.data)
    if serializer_class.is_valid():
        serializer_class.save()
        data1 = "Received Data successfully"
        programmable_parameters = ProgrammableParameters.objects.filter(device_id = 2)
        print("programmable_parameters - ", programmable_parameters)

        serializer_programmable_parameters = ProgrammableParameterSerializer(programmable_parameters , many=True)
        
        # if serializer_device_class.is_valid():
        # print("serializer_device_class - ", serializer_device_class.data)
        return Response(serializer_programmable_parameters.data)
    else:
        data = "Sorry, Please check and try again"

        return Response(serializer_class.errors)


@api_view(['POST'])
def addDevice(request):
    serializer_class = DeviceSerializer(data=request.data)
    if serializer_class.is_valid():
        serializer_class.save()
        return Response(serializer_class.data)
    else:
        return Response(serializer_class.errors)


