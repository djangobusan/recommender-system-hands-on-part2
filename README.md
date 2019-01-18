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
    
4. Model -> View -> Template로 구성
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



