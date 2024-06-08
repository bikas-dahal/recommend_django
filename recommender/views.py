from django.shortcuts import render
from .models import Course

# Create your views here.

def index(request):
    courses = Course.objects.all()
    context = {
        'name' : 'Recommender System',
        'courses': courses
    }
    return render(request, 'index.html', context)