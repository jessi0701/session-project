from django.shortcuts import render,redirect
from .models import Movie,Score
from .forms import ScoreForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
# Create your views here.
def list(request):
    movies = Movie.objects.all()
    
    # URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    # API_KEY = 'd2ade5d0aa053b15bfe8c12450f6871b'
    # api_key = '166adf4bc35ebd57d55282ce84cae4fe'
    # today = '20171101'
    # # 완성된 요청 주소
    # request_url = f'{URL}?key={API_KEY}&targetDt={today}'
    # # 주소로 요청한 결과를 res에 저장
    # res = requests.get(request_url)
    # # 요청결과인 res에서 영화 10개가 담긴 list를 movie_list에 저장
    # movie_list = res.json().get('boxOfficeResult').get('dailyBoxOfficeList')
    
    # # csvfile = open("movie_list.csv",'a+',newline='')
    # # csvwriter = csv.writer(csvfile)
    # for movie in movie_list:
    #     # print(movie)
    #     movie_nm = movie.get('movieNm')
    #     movie_cd = movie.get('movieCd')
        
    #     #영화 상세정보 URL
    #     detail_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
    #     themoviedb_URL = 'https://api.themoviedb.org/3/search/movie'
        
    #     #상세정보 완성 요청주소
    #     request_detail_url = f'{detail_URL}?key={API_KEY}&movieCd={movie_cd}'
    #     request_themoviedb_url = f'{themoviedb_URL}?api_key={api_key}&query={movie_nm}&language=ko-kr'
        
    #     #상세정보 요청
    #     themoviedb_res = requests.get(request_themoviedb_url)
    #     detail_res = requests.get(request_detail_url)
        
    #     themovie_detail_res = themoviedb_res.json().get('results')[0]
    #     detail_movies = (detail_res.json().get('movieInfoResult').get('movieInfo'))
    #     detail_genre = (detail_res.json().get('movieInfoResult').get('movieInfo').get('genres'))
    #     index = 0
    #     for genre in detail_genre:
    #         if index == 1:
    #             break
    #         movie_genre = genre.get("genreNm")
    #         index +=1
            
    #     # print(themovie_detail_res)
    #     movie_actor = []
    #     movie_name = detail_movies.get('movieNm') #영화 이름
    #     movie_date = detail_movies.get('openDt') #개봉년도
    #     movie_director = detail_movies.get('directors')[0].get('peopleNm') #감독
    #     movie_actor_list = detail_movies.get('actors') #배우
    #     movie_overview = themovie_detail_res.get('overview')#상세정보
    #     movie_poster_url = f'https://image.tmdb.org/t/p/w500{themovie_detail_res.get("poster_path")}'#포스터
    #     movie_average = 0#평점
        
    #     index= 0
    #     for i in movie_actor_list:
    #         if index == 3:
    #             break
    #         if i:
    #             movie_actor.append(i.get("peopleNm"))
    #             index +=1
    #     movie_audits = detail_movies.get('audits')[0].get('watchGradeNm') #관람가
    
    paginator = Paginator(movies, 8)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    return render(request, 'movies/list.html',{'movies':movies})
    
def detail(request,id):
    movie = Movie.objects.get(id=id)
    score_form = ScoreForm()
    total_score = 0
    # print(movie.score_set.all())
    for score in movie.score_set.all():
        total_score += score.value
    if len(movie.score_set.all())==0:
        total_score = 0
    else:
        total_score /= len(movie.score_set.all())
        total_score = round(total_score,2)
    movie.average = total_score
    movie.save()
    return render(request,'movies/detail.html',{'movie':movie,'score_form':score_form, 'total_score':total_score})

@login_required
@require_POST
def score_create(request,id):
    value = request.POST.get('value')
    score_form = ScoreForm(request.POST)
    if score_form.is_valid():
        score = score_form.save(commit=False)
        score.user = request.user
        score.value = value
        score.movie = Movie.objects.get(id=id)
        score_form.save()
        return redirect("movies:detail",id)
        
@login_required
def score_delete(request, movie_id, score_id):
    score = Score.objects.get(id=score_id)
    if score.user == request.user:
        score.delete()
    return redirect("movies:detail", movie_id)
    
@login_required 
def score_edit(request, movie_id, score_id):
    score = Score.objects.get(id=score_id)
    value = request.POST.get('value')
    if request.method == 'POST':
        score_form = ScoreForm(request.POST, instance=score)
        if score_form.is_valid():
            score.value = value
            score_form.save()
            return redirect("movies:detail",movie_id)
    else:
        score_form = ScoreForm(instance=score)
    return render(request, "movies/edit.html",{'score_form':score_form})
    
@login_required 
def like(request, movie_id):
    me = request.user
    movie = Movie.objects.get(id=movie_id)
    
    if movie in me.mymovies.all():
        me.mymovies.remove(movie)
    else:
        me.mymovies.add(movie)
    return redirect('movies:detail',movie_id)
    
def search(request):
    word = request.GET.get('search_keyword')
    movies = Movie.objects.filter(title__icontains=word)
    
    paginator = Paginator(movies, 8)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    return render(request, "movies/search.html",{'movies':movies})

def classification(request):
    word = request.GET.get('genre')
    movies = Movie.objects.filter(genre=word)
    
    paginator = Paginator(movies, 8)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    return render(request, "movies/search.html",{'movies':movies})
    
    
        