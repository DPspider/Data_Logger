from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from dashboard.models import ProgrammableParameters, UserProfile, Devices, Report

class  ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class  DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = '__all__'

class  ProgrammableParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammableParameters
        fields = '__all__'