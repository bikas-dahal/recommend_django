import django_filters 
from django_filters.filters import CharFilter

from .models import Course

class CourseFilter(django_filters.FilterSet):
    course_title = CharFilter(
        lookup_expr='icontains'
    )
    class Meta:
        model = Course
        fields = ['course_title']
        
        