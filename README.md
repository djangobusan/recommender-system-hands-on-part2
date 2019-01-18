# Django로 만드는 '영화 리뷰 시스템'

## 왜 영화 리뷰 시스템을 만드나?

1. ML/DL 등을 학습하여 자신만의 서비스를 만들 때 필요한 기본 기술인 Web 기술을 연습하기 위한 좋은 예제
2. 영화 리뷰 데이터가 구하기 쉽고, 다양한 예제로 변경 가능함(MovieLends)
3. Django이 기본적인 기능만으로 충분히 구현 가능함

## 만드는 순서

1. 파이썬 개발 환경 구성
    * Python(>= 3 and =< 3.6)
    * VSCode 설치
        * 플러그인 설치; Python, Django Template, Django Snippets
    * Python venv 환경
    ```
    $ mkdir movie-recommander-system
    $ cd movie-recommander-system
    $ python -m venv venv
    $ venv\Scripts\activate
    $ pip install django
    $ git init
    $ code .
    ```

    * `.gitignore` 설정(https://www.gitignore.io/)
    ```
    $ code .gitignore
    -- venv, Python, Django, VisualStudioCode > Crate
    -- All Selecte -> C-c -> C-p
    $ dir
    01/19/2019  02:59 AM    <DIR>          .
    01/19/2019  02:59 AM    <DIR>          ..
    01/19/2019  03:05 AM             3,087 .gitignore
    01/19/2019  02:57 AM    <DIR>          venv
               1 File(s)          3,087 bytes
               3 Dir(s)  2,343,711,342,592 bytes free
    ```

2. 프로젝트 생성 및 구성
    * `View -> Terminal`
    ```
    $ django-admin startproject settings .
    $ python manage.py startapp reviews
    ```

3. 프로젝트 설정
    * 디렉토리 설정
    ```
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')    
    ```

    * INSTALLED_APPS
    ```
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'reviews',
    ]    
    ```

    * TEMPLATES
    ```
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [TEMPLATE_DIR,],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]    
    ```

    * STATICFILES_DIRS
    ```
    STATICFILES_DIRS = [STATIC_DIR,]
    ```

    * `static`, `templates` 폴더 생성
    ```
    (venv) $ mkdir static
    (venv) $ mkdir templates
    ```

    * Static 파일(bootstrap, jQuery)을 다운받아서 `static`에 압축 해제
    

    * migrate
    ```
    (venv) $ python manage.py migrate
    ```

    * runserver
    ```
    (venv) $ python manage.py runserver
    ```
    
4. Model
    * 모델 분석
        * movies.csv
        ```
        //movieId,movieName,genres
        176601,Black Mirror (2011),(no genres listed)
        176621,Boniface's Holiday (1965),Animation|Children|Comedy|Romance
        ```
        * ratings.csv
        ```
        userId,movieId,rating,timestamp
        1,1,4.0,964982703
        ```
        * tags.csv
        ```
        userId,movieId,tag,timestamp
        2,60756,funny,1445714994
        ```
    * 모델 작성
    ```
    // genere
    from django.db import models

    class genre(models.Model):
        name = models.CharField(max_length=64)

        def __str__(self):
            return self.name
    
    // movie
    class movie(models.Model):
        movieId = models.CharField(max_length=16, primary_key=True, db_column='movieId')
        title = models.CharField(max_length=128)
        year = models.IntegerField(null=True)

        def __str__(self):
            return self.title

    // tags
    class rating(models.Model):
        userId = models.CharField(max_length=16)
        movieId = models.CharField(max_length=16)
        rate = models.DecimalField(decimal_places=2, max_digits=4)
        timestamp = models.DateTimeField()

        def __str__(self):
            return "userId: {}, movieId: {}, rating: {}".format(self.userId, self.movieId, self.rate)
    ```

    * 모델 연결
    ```
    // movie
    class movie(models.Model):
        genres = models.ManyToManyField(genre, related_name='movies', db_table='movie_genre')
    ```

    * 사용자
    ```
    from django.contrib.auth.models import User
    class UserInfo(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)

        def __str__(self):
            return self.user.username    
    ```

5. URL 추가
    * `reviews` 추가
    ```
    from django.urls import path
    from . import views

    app_name = 'reviews'

    urlpatterns = [
        path('', views.index, name='Index'),
    ]    
    ```

    * 프로젝트에 추가
    ```
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('reviews.urls')),
    ]
    ```

6. View 작성
```
from django.shortcuts import render

def index(request):
    return render(request, 'reviews/index.html', {})    

```

7. Tempates 작성
    * base.html 작성
    ```
    <!DOCTYPE html>
    <html>
        <head>
            {% load staticfiles %}
            <title>DBUG - 영화 추천 시스템 만들기 Part2</title>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="{% static "css/bootstrap.min.css" %}">
            <style>
            body {
                padding-top: 3.5rem;
            }
            </style>
        </head>

        <body>
            <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
                <a class="navbar-brand" href="#">MovieReview</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarsExampleDefault">
                    <ul class="navbar-nav mr-auto">
                        <li class="nav-item active">
                            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                        </li>
                    </ul>
                    <form class="form-inline my-2 my-lg-0">
                    <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                    </form>
                </div>
            </nav>

        <main>
            <div class="container">
                {% block body_block %}
                {% endblock body_block %}							
            </div>					
        </main>

        <script type="text/javascript" src="{% static "js/jquery-3.3.1.min.js" %}"></script>
        <script type="text/javascript" src="{% static "js/bootstrap.bundle.min.js" %}"></script>
        </body>
    </html>
    ```

    * reviews/index.html
    ```
    {% extends "base.html" %}
    {% block body_block %}
        <div class="jumbotron">
            <h1>Hello, Django</h1>
        </div>
    {% endblock body_block %}
	    
    ```

8. 로그인 / 가입 처리
    * reviews/urls.py
    ```
	path('', views.index, name='UserLogin'),
    ```

    * reviews/form.py
    ```
    from django import forms
    from django.contrib.auth.models import User
    from .models import UserInfo

    class UserForm(forms.ModelForm):
        password = forms.CharField(widget=forms.PasswordInput())
        class Meta:
            model = User
            fields = ('username', 'email', 'password')
    ```

    * reviews/view.py
    ```
    from django.shortcuts import render
    from django.urls import reverse
    from django.http import HttpResponseRedirect, HttpResponse
    from django.contrib.auth import authenticate, login, logout

    from .forms import UserForm

    def index(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('reviews:UserLogin'))
                else:
                    return HttpResponse("ACCOUNT NOT ACTIVE")
            else:
                print("Someone tried to loggin and failed!")
                print("Username: {} and Password: {}".format(username, password))
                return HttpResponse("INVALID LOGIN DETAILS SUPPLIED")
        else:
            return render(request, 'reviews/index.html', {})    

    def register(request):
        registered = False

        if request.method == 'POST':
            user_form = UserForm(data=request.POST)

            if user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                registered = True
            else:
                print(user_form.errors)
        else:
            user_form = UserForm()

        return render(request, 'reviews/registration.html', {'registered': registered, 'user_form': user_form})

    ```

    * base.html
    ```
    <!DOCTYPE html>
    <html>
        <head>
            {% load staticfiles %}
            <title>DBUG - 영화 추천 시스템 만들기 Part2</title>
            <meta charset="utf-8">
            <link rel="stylesheet" type="text/css" href="{% static "css/bootstrap.min.css" %}">
            <style>
            body {
                padding-top: 3.5rem;
            }
            </style>
        </head>

        <body>
            <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
                <a class="navbar-brand" href="{% url 'reviews:UserLogin' %}">MovieReview</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarsExampleDefault">
                    <ul class="navbar-nav mr-auto">
                        <li class="nav-item active">
                            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                        </li>
                        {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="#">Logout</a>
                        </li>
                        {% endif %}
                        {% if not user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'reviews:Registration' %}">Register</a>
                        </li>
                        {% endif %}					
                    </ul>

                    <form class="form-inline my-2 my-lg-0">
                    <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                    </form>
                </div>
            </nav>

        <main>
            <div class="container">
                {% block body_block %}
                {% endblock body_block %}							
            </div>					
        </main>

        <script type="text/javascript" src="{% static "js/jquery-3.3.1.min.js" %}"></script>
        <script type="text/javascript" src="{% static "js/bootstrap.bundle.min.js" %}"></script>
        </body>
    </html>    
    ```

    * index.html
    ```
    {% extends "base.html" %}
    {% block body_block %}
        <div class="jumbotron">
            <h1>Please Login</h1>
            <form action="{% url 'reviews:UserLogin' %}" method="post">
                {% csrf_token %}
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" name="username" id="username" placeholder="Enter Username" class="form-control">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" name="password" id="password" placeholder="Enter Password" class="form-control">
                </div>
                <button type="submit" value="Login" class="btn btn-primary">Login</button>
            </form>
        </div>
    {% endblock body_block %}
	    
    ```

    * registration.html
    ```
    {% extends "reviews/index.html" %}

    {% block body_block %}

    <div class="jumbotron">
        {% if registered %}
            <h1>Thank you for registering</h1>
        {% else %}
            <h1>Register Here!</h1>
            <h3>Fill out the form:</h3>
            <form method="post">
                {% csrf_token %}
                {% for field in user_form %}
                <div class="form-group">
                    <input type={{ field.name }} name={{ field.name }} id={{ field.name }} placeholder={{ field.name }} class="form-control">
                </div>
                {% endfor %}
                <button type="submit" value="Register">registered</button>
            </form>
        {% endif %}
    </div>

    {% endblock %}    
    ```