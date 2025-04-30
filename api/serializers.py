from rest_framework import serializers
from notesapp.models import Student
from employee.models import Employee

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = ['student_id', 'name', 'branch']
        fields = '__all__'  # This will include all fields in the model

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'  # This will include all fields in the model