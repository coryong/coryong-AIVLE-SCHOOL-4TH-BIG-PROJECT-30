DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 사용할 데이터베이스 엔진
        'NAME': 'Connect', # 데이터베이스 이름 
        'USER': 'root', # 접속할 Database 계정 아이디 ex) root
        'PASSWORD': 'aivle',  # 접속할 Database 계정 비밀번호 ex) 1234
        'HOST': 'localhost',   # host는 로컬 환경에서 동작한다면 ex) localhost
        'PORT': '3306', # 설치시 설정한 port 번호를 입력한다. ex) 3306
    }
}

# settings.py에 있던 시크릿 키를 아래 ''안에 입력한다.
SECRET_KEY ='django-insecure-w$=)%c6n)-w(buxrm9jkru*=gumfnlc5l5(bxka__k+8iw!m&v'