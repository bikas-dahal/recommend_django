from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'name' : 'Recommender System',
    }
    return render(request, 'index.html', context)