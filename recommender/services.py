import pandas 
from qdrant_client import QdrantClient
from qdrant_client.models import models 
from sentence_transformers import SentenceTransformer
import pickle

# Load and prepare data 
def load_data(data):
    return pandas.read_csv(data)


def prepare_data(df):
    docx =df['course_title'].tolist()
    payload = df[['course_id', 'course_title', 'subject', 'price']].to_dict()
    return docx, payload


def save_vectors(vectors):
    with open('vectorized_courses.pickle', 'wb') as f: 
        pickle.dump(vectors, f)
        
        
def load_vectors(vector_file):
    with open('vector_file', 'rb') as f: 
        my_object = pickle.load(f)
    return my_object
        

# Create a vectorDB client

client = QdrantClient(path = 'vector_database.db')
client.recreate_collection(collection_name = 'courses_collection',
                           vectors_config = models.VectorParams(
                               size = 384,
                               distance = models.Distance.COSINE
                           ))


# Vectorized data and create word embedding 
model = SentenceTransformer('all-MiniLM-L6-v2')

df = load_data('udemy_courses.csv')

docx, payload = prepare_data(df)
# print(docx)
print(payload)

vectors = model.encode(docx, show_progress_bar=True)
save_vectors(vectors)


# Store in vectorDB collection
client.upload_collection(
    collection_name = 'courses_collection',
    vectors=vectors,
    payload=payload,
    ids=None,
    batch_size =256
)

vectorized_text = model.encode('python').tolist()

result = client.search(collection_name = 'courses_collection',
                       query_vector=vectorized_text,
                       limit = 5)

print(result)
