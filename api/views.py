from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from notesapp.models import Student
from .serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employee.models import Employee
from .serializers import EmployeeSerializer
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework import viewsets
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer
from .paginations import CustomPagination
from employee.customfilter import CustomFilter
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.
def studentsViewForManual(request):
    students = Student.objects.all() # Fetch all students from the database it is a QuerySet
    # print(students)
    # print(type(students))
    students = list(students.values()) # Convert the QuerySet to a list of dictionaries - manual Serialization 
    return JsonResponse(students, safe=False)

@api_view(['GET','POST']) # This decorator is used to specify the allowed HTTP methods for the view
def studentsView(request):
    if request.method == 'GET':
        students = Student.objects.all() # Fetch all students   from the database it is a QuerySet
        serializer = StudentSerializer(students, many=True) # Convert the QuerySet to a list of dictionaries - Serialization
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(): # in-built method to check if the data is valid
            serializer.save() # this method saves the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET","PUT","DELETE"]) # This decorator is used to specify the allowed HTTP methods for the view
def studentDetailView(request, id): #pk is the path parameter that represents the primary key of the student
    try:
        student = Student.objects.get(pk=id) # Fetch the student with the given primary key (id)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student) # Convert the student object to a dictionary - Serialization
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Employeee(APIView):
    def get(self, request):
        employees = Employee.objects.all() # Fetch all employees from the database it is a QuerySet
        serializer = EmployeeSerializer(employees, many=True) # Convert the QuerySet to a list of dictionaries - Serialization
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(): # in-built method to check if the data is valid
            serializer.save() # this method saves the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmployeeDetails(APIView):

    def get_object(self, id):
        try:
            employee = Employee.objects.get(pk=id) # Fetch the employee with the given primary key (id)
        except Employee.DoesNotExist:
            raise Http404("Employee not found")
            # return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        return employee

    def get(self, request, id):
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        employee = self.get_object(id)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        employee = self.get_object(id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

#Mixins Class Based Views
#ListModelMixin - list  
#CreateModelMixin - create
#RetrieveModelMixin - retrieve
#UpdateModelMixin - update
#DestroyModelMixin - destroy
#GenericAPIView - Provides the base functionality for all generic views

class EmployeesMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request) # coming from ListModelMixin

    def post(self, request):
        return self.create(request) # coming from CreateModelMixin


class EmployeeDetailMixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk) # coming from RetrieveModelMixin

    def put(self, request, pk):
        return self.update(request, pk) # coming from UpdateModelMixin

    def delete(self, request, pk):
        return self.destroy(request, pk) # coming from DestroyModelMixin
    
#Generics
#ListAPIView - list
#CreateAPIView - create
#RetrieveAPIView - retrieve
#UpdateAPIView - update
#DestroyAPIView - destroy
#ListCreateAPIView - list and create
#RetrieveUpdateAPIView - retrieve and update
#RetrieveUpdateDestroyAPIView - retrieve, Update and destroy
class EmployeesGenerics(generics.ListCreateAPIView): # generics.ListAPIView, generics.CreateAPIView -> ListCreateAPIView
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    

class EmployeeDetailGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk' # This is the default value, so you can omit this line if you want

#ViewSets
#ViewSets are a way to define the logic for a set of related views in a single class
#viewsets.ViewSet - A base class for all viewsets like list, create, retrieve, update, destroy

class EmployeesViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk) # default method to get the object
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#viewsets.ModelViewSet - A viewset that provides CRUD operations for a model and takes only queryset and serializer_class as arguments
# and a lookup_field which is optional
class Employees(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk' # This is the default value, so you can omit this line if you want
    pagination_class = CustomPagination # Custom pagination class
    # filterset_fields = ['designation'] # Filter the queryset based on the fields in the model
    filterset_class = CustomFilter # Custom filter class

# Blogs and Comments ViewSets

class BlogsView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk' # This is the default value, so you can omit this line if you want

class CommentsView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk' # This is the default value, so you can omit this line if you want