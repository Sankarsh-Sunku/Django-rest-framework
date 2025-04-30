from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', views.Employees, basename='employee')
router.register('blogs', views.BlogsView, basename='blogs')
router.register('comments', views.CommentsView, basename='comments')


urlpatterns = [
    path('students/', views.studentsView, name='students'),
    path('students/<int:id>/', views.studentDetailView, name='student-id'),
    # path('employees/', views.Employees.as_view(), name='employees'),
    # path('employees/<int:pk>/', views.EmployeeDetail.as_view(), name='employees-id'),
    path('', include(router.urls), name='api-urls'),
    # path('blogs/',views.BlogsView.as_view(), name='blogs'),
    # path('comments/',views.CommentsView.as_view(), name='comments'),
]