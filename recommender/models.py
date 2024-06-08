from django.db import models

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
        ('Musical Instrument', )
    ]
    
    course_id = models.IntegerField(max_length =12, blank=True, null=True)
    course_title = models.CharField(max_length=255, blank=True, null=True)
    