from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
# from .models import User
from django.contrib.auth import get_user_model
import json
from .forms import UserCustomCreationForm
from movies.models import Movie
# Create your views here.

def list(request):
    users = User.objects.all()
    return render(request, 'accounts/list.html',{'users':users})
    
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:list')
    if request.method == 'POST':
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect('movies:list')
    else:
        user_form = UserCustomCreationForm()
    context = {'form': user_form}
    return render(request, 'accounts/forms.html', context)
    
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:list')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('movies:list')
    else:
        login_form = AuthenticationForm()
    context = {'form': login_form}
    return render(request, 'accounts/forms.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:list')
    
@login_required
def detail(request, id):
    User = get_user_model()
    user_info = User.objects.get(id=id)
    user_movies = user_info.mymovies.all()
    my_dict = {}
    favorite_genre = ""
    number = -1
    
    recommend_movie=[]
    if user_movies:
        for movie in user_movies:
            if my_dict.get(movie.genre) == None:
                my_dict[movie.genre] = 1
            else:
                my_dict[movie.genre] += 1
    
            
    
        for genre in my_dict.keys():
            if my_dict[genre] > number:
                number = my_dict[genre]
                favorite_genre = genre
                
        movies = Movie.objects.filter(genre=favorite_genre).order_by('?')
        
        
        while len(recommend_movie) < 3:
            movie = movies.first()
            print(movie)
            if movie not in recommend_movie:
                recommend_movie.append(movie)
                # if len(recommend_movie) == len(movies):
                #     break
            # print(len(recommend_movie), len(movies))
        my_dict = json.dumps(my_dict)
        
    else:
        pass
            
        
    
    return render(request, 'accounts/detail.html',{'user_info':user_info, 'my_dict':my_dict,'recommend_movie':recommend_movie,'favorite_genre':favorite_genre})
