import pandas 
import pickle
import os

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
    with open(os.path.join(vector_file), 'rb') as f: 
        my_object = pickle.load(f)
    return my_object