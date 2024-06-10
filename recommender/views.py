from django.shortcuts import render
from .models import Course
from django.core.paginator import Paginator

from .forms import RecommenderForm
from .filters import CourseFilter


from qdrant_client import QdrantClient
from qdrant_client.models import models 
from sentence_transformers import SentenceTransformer
from .utils import load_data, prepare_data, load_vectors


# Create a vectorDB client

client = QdrantClient(':memory:')
client.recreate_collection(collection_name = 'courses_collection',
                           vectors_config = models.VectorParams(
                               size = 384,
                               distance = models.Distance.COSINE
                           ))


# Vectorized data and create word embedding 
model = SentenceTransformer('all-MiniLM-L6-v2')

df = load_data('udemy_courses.csv')

docx, payload = prepare_data(df)

vectors = load_vectors('vectorized_courses.pickle')

# Store in vectorDB collection
client.upload_collection(
    collection_name = 'courses_collection',
    vectors=vectors,
    payload=payload,
    ids=None,
    batch_size =256
)



# Create your views here.

def index(request):
    courses = Course.objects.all()
    
    search_filter = CourseFilter(
        request.GET,
        queryset=courses
    )
    
    search_item = request.GET.get('course_title', "")
    
    courses = search_filter.qs
    
    paginator = Paginator(courses, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        'name' : 'Recommender System',
        'courses': courses,
        'search_filter': search_filter,
        'page_obj': page_obj,
        'search_item': search_item
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
    
    
def recommend_view(request):
    if request.method == 'POST':
        form = RecommenderForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            
            vectorized_text = model.encode(search_term).tolist()

            search_result = client.search(collection_name = 'courses_collection',
                                query_vector=vectorized_text,
                                limit = 5)
            
            courses = [suggestion.payload for suggestion in search_result]
            scores = [{'score': suggestion.score} for suggestion in search_result]
            result = [{**courses[i], **scores[i]} for i in range(len(courses))]
            
            context = {
                'result': result, 'form': form, 'search_term': search_term
            }
            return render(request, 'recommended.html', context)
    
    else:
        form = RecommenderForm()
    
    context = {
        'form': RecommenderForm(),
    }
    
    return render(request, 'recommended.html', context)