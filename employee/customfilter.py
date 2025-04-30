import django_filters 
from .models import Employee


class CustomFilter(django_filters.FilterSet):
    designation = django_filters.CharFilter(field_name='designation', lookup_expr='iexact')
    emp_name = django_filters.CharFilter(field_name='emp_name', lookup_expr='icontains')
    # id = django_filters.RangeFilter(field_name='id')
    id_min = django_filters.CharFilter(method='filter_by_id_range', label = 'from employee id')
    id_max = django_filters.CharFilter(method='filter_by_id_range', label = 'to employee id')

    class Meta:
        model = Employee
        fields = ['designation', 'emp_name', 'id_min', 'id_max']

    def filter_by_id_range(self, queryset, name, value): #queryset comes from the filterset
        if name == 'id_min':
            return queryset.filter(employee_id__gte=value)
        elif name == 'id_max':
            return queryset.filter(employee_id__lte=value)
        return queryset
    
