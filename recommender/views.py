from django.shortcuts import render
from .models import Course
from django.core.paginator import Paginator

from .filters import CourseFilter

# Create your views here.

def index(request):
    courses = Course.objects.all()
    
    search_filter = CourseFilter(
        request.GET,
        queryset=courses
    )
    
    courses = search_filter.qs
    
    paginator = Paginator(courses, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        'name' : 'Recommender System',
        'courses': courses,
        'search_filter': search_filter,
        'page_obj': page_obj,
    }
    return render(request, 'index.html', context)

def read_course(request, pk):
    course = Course.objects.get(pk=pk)
    context = {
        'course': course
    }
    return render(
        request,
        'read_course.html',
        context
    )