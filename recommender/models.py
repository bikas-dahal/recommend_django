from django.db import models
import datetime

# Create your models here.

class Course(models.Model):
    
    LEVELS = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    SUBJECT = [
        ('Business Finance', 'Business Finance'),
        ('Computer Science', 'Computer Science'),
        ('Musical Instrument', 'Musical Instrument'),
        ('Graphic Design', 'Graphic Design')
    ]
    
    course_id = models.IntegerField(max_length =12, blank=True, null=True)
    course_title = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(null=True, blank=True, max_length=1000)
    is_paid = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=1000, blank=True, null=True)
    subscribers = models.IntegerField(blank=True, null=True)
    num_lectures = models. IntegerField(blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=100, null=True, blank=True, choices=LEVELS)
    content_duration = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=500, null=True, blank=True, choices=SUBJECT)
    published_timestamp = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    @property
    def published_on(self):
        date_format = '%Y-%m-%dT%H:%M:%SZ'
        datetime_object = datetime.strptime(self.published_timestamp, date_format)
        return datetime_object