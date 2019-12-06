uWSGI, Nginx, AWS EC2 사용하여 Django 배포
================

이 문서는 Django 앱을 uWSGI와 Nginx를 사용하여 배포하는 방법에 대해서 배우겠다. 앞서 AWS EC2에 Django
앱을 설치하는 방법에 대해서 배웠다. 배포를 할때 새로운 유저그룹을 만들어서 하는게 보안상으로 더 안전하다. 그러나 여기서는
AWS EC2의 기본 유저인 ubuntu 유저를 사용하겠다.

## 시작전

EC2 서버에 접속을 한 뒤 필요한 패키지들을 설치한다. 그 외에 필요한 패키지 설치는 [AWS Ubuntu EC2 와
Python
Django](https://github.com/whoareyouwhoami/ProjectTellus/blob/master/documentation/python_django.md)를
참고하길 바란다.

    sudo apt-get update
    sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev libpcre3 libpcre3-dev

## uWSGI 설치

**uwsgi 패키지 설치**

예시를 위해 Django 프로젝트 이름과 가상환경 이름을 `srv/ProjectFolder`안에 아래와 같이 만들었다고 가정하자.

  - 가상환경 : `prj_venv`
  - 프로젝트 : `someproject`

먼저 Django 프로젝트가 있는 폴더로 이동해 가상환경을 활성화 해준다.

    source prj_venv/bin/activate

그리고 `pip`를 사용하여 `uwsgi`를 설치해준다.

    pip install uwsgi

그 후에 `conf`, `run`, `log` 파일을 만들어 준다. 여기서는 프로젝트 안에 설치할 것이다. 먼저 프로젝트로 이동
후 폴더를 만든다.

    # 프로젝트 폴더 이동
    cd someproject
    
    # 이동 후
    mkdir conf run log

그리고 폴더 안에 들어가 `touch log/uwsgi.log`를 실행해 `log`폴더에 `uwsgi.log`파일을 만든다. 그
다음 `run` 폴더와 `log` 폴더에 어느 유저나 그룹이 파일을 변경하고 실행할 수 있게 허락을 해준다.

    sudo chmod 777 /srv/ProjectFolder/someproject/run
    sudo chmod 777 /srv/ProjectFolder/someproject/log

**uwsgi.ini 설정** `conf` 파일로 이동 후 `nano uwsgi.ini`를 사용하여 `uwsgi.ini` 파일을
만들어 아래 코들들 붙여 넣으면 된다. 필요한 부분을 수정하면 된다.

    [uwsgi]
    
    uid = ubuntu
    gid = ubuntu
    
    # 프로젝트 이름 
    project_name = someproject
    
    # 프로젝트가 있는 경로 
    base_dir = /srv/ProjectFolder/
    
    # 가상환경이 있는 경로 
    virtualenv = %(base_dir)/prj_venv/
    
    # manage.py가 있는 폴더 
    chdir = %(base_dir)/%(project_name)/
    
    # wsgi 모듈
    module =  %(project_name).wsgi:application
    
    master = true
    processes = 4
    post-buffering = 204800
    thunder-lock = True
    uwsgi-socket = %(base_dir)/%(prject_name)/%(prject_name).sock
    chmod-socket = 666
    socket-timeout = 300
    reload-mercy = 8
    reload-on-as = 512
    harakiri = 50
    max-requests = 5000
    vacuum = true
    disable-logging = True
    logto = %(base_dir)/%(project_name)/log/uwsgi.log
    log-maxsize = 20971520
    log-backupname = %(base_dir)/%(project_name)/log/old-uwsgi.log
    touch-reload = %(base_dir)/
    max-worker-lifetime = 300

이제 `uwsgi.ini` 파일이 정상적으로 돌아가는지 아래 코드를 실행해서 확인하겠다.

``` 
 uwsgi --ini /srv/ProjectFolder/someproject/conf/uwsgi.ini
```

uwsgi에 대한 로그를 확인하고 싶으면 `log` 파일에 들어가서 `cat uwsgi.log`을 통해 볼 수 있다.

**uwsgi.service 설정** 여기서는 우분투 서비스 매니저인 `systemd`를 사용하여 서비스를 등록할 것이다.

    sudo nano /etc/systemd/system/uwsgi.service

아래 코드를 복사하여 프로젝트 폴더 이름과 가상환경 이름을 변경해주면 된다.

    [Unit]
    Description=uWSGI instance to serve updateMe project
    After=network.target
    
    [Service]
    User=ubuntu
    Group=ubuntu
    WorkingDirectory=/srv/ProjectFolder/someproject/
    Environment="PATH=/srv/ProjectFolder/prj_venv/bin"
    ExecStart=/srv/ProjectFolder/prj_venv/bin/uwsgi --ini /srv/ProjectFolder/someproject/conf/uwsgi.ini
    Restart=always
    KillSignal=SIGQUIT
    Type=notify
    NotifyAccess=all
    
    [Install]
    WantedBy=multi-user.target

마지막으로 `systemd`를 변경했으니 변경된 구성들이 잘 돌아가게 새로고친 후 `uwsgi`가 시스템에서 돌아갈 수 있게
활성화 해준다.

    sudo systemctl daemon-reload
    sudo systemctl enable uwsgi

아래 코드들을 통해 `uwsgi`를 시작, 재가동, 중단 그리고 상태를 확인 할 있다.

**uwsgi 시작**

    sudo service uwsgi start

**uwsgi 재가동**

    sudo service uwsgi restart

**uwsgi 중단**

    sudo service uwsgi stop

**uwsgi 상태 확인**

    sudo service uwsgi status

<br>

## NGINX 설치

이제 NGINX 설치법에 대해서 알아보겠다. NGINX를 설치하면 기본으로 포트 80을 들을 수 있도록 구성이 되어있어 바로
브라우저를 켜서 프로젝트 주소를 입력해서 정상적으로 설치가 되었느지 확인할 수 있다.

    sudo apt-get update
    sudo apt-get install nginx

NGINX를 설치하면 기본적으로 `sites-available` 폴더와 `sites-enabled` 폴더가 있다. 그러나 여기서는
따로 `nginx-uwsgi.conf` 파일을 만들어서 브라우저에서 받는 요청을 uWSGI서버에 연결을 할 수 있게 설정을 할
것이다. 먼저 기본으로 설치된 폴더를 제거한 후 실행한다.

    # 기본 폴더 제거
    sudo rm -rf /etc/nginx/sites-available/default
    sudo rm -rf /etc/nginx/sites-enabled/default
    
    # nginx-uwsgi.conf 생성 
    sudo nano /etc/nginx/sites-available/nginx-uwsgi.conf

`nginx-uwsgi.conf` 파일에 아래와 같이 복사하고 필요한 부분을 바꾸거나 채워 넣는다.

    upstream someproject_dev {
        server unix:/srv/ProjectName/someproject/someproject.sock;
    }
    
    server {
        listen 80;
        server_name <IP 주소>;
        charset utf-8;
    
        client_max_body_size 128M;
    
        location /static {
        # static 파일이 있는 경로 
        # staticfile : Django 프로젝트에 사용한 static 파일을 모아둔 폴더 이름
            alias /srv/ProjectName/someproject/staticfile;
        }
    
        location /media {
        # media 파일이 있는 경로
            alias /srv/ProjectName/someproject/mediafile;
        }
    
        location / {
            include uwsgi_params;
            uwsgi_pass someproject_dev;
            uwsgi_read_timeout 300s;
            uwsgi_send_timeout 300s;
        }
    
        access_log /srv/ProjectName/someproject/log/nginx-access.log;
        error_log /srv/ProjectName/someproject/log/nginx-error.log;
    }

이거를 마친 후에는 심볼릭 링크를
    만들어준다.

    sudo ln -s /etc/nginx/sites-available/nginx-uwsgi.conf /etc/nginx/sites-enabled/nginx-uwsgi.conf

마지막으로 uWSGI 설치에서 했던거처럼 다음 코드를 실행해서 nginx를 활성화 해주면 된다.

    sudo systemctl daemon-reload
    sudo systemctl enable nginx

**nginx 시작**

    sudo service nginx start

**nginx 테스트** nginx 시작 후 테스트를 해본다. OK가 반환되면 정상적으로 가동된 것이다.

    sudo nginx -t

**nginx 재가동**

    sudo service nginx restart

**nginx 중단**

    sudo service nginx stop

**nginx 상태 확인**

    sudo service nginx status

나중에 서버를 돌리면 접근하는 로그 또는 에러 로그는 아까 만든 `log` 파일에 있으므로 아래의 코드를 실행시켜 확인할 수
있다.

``` 
 cat /srv/ProjectName/someproject/log/nginx-access.log
 cat /srv/ProjectName/someproject/log/nginx-error.log
```

## 마무리

지금까지 AWS EC2 Ubuntu를 사용하여 Django 프로젝트를 uWSGI와 NGINX 웹 서버를 설치해 배포하는 방법에
대해서 알아봤다.
