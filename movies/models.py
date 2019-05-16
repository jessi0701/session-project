from django.db import models
from django.conf import settings
# Create your models here.

# class Genre(models.Model):
#     name = models.CharField(max_length=20)
    
#     def __str__(self):
#         return self.name
        
class Movie(models.Model):
    title = models.CharField(max_length=30)
    date = models.IntegerField() 
    actors = models.CharField(max_length = 50)
    audits = models.CharField(max_length=20)
    director = models.CharField(max_length = 15)
    description = models.TextField()
    poster_url = models.TextField()
    average = models.FloatField()
    genre = models.CharField(max_length=15)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="mymovies",blank=True)
    poster2_url = models.CharField(max_length=100)
    
    # def __str__(self):
    #     return self.title
      
    
class Score(models.Model):
    content = models.CharField(max_length=100)
    value = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
