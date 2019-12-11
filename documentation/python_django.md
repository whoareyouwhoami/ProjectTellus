AWS Ubuntu EC2 와 Python Django
================

### AWS EC2 사용하여 Django 앱 배포

이 문서는 AWS EC2 Ubuntu 18.04 LTS를 사용하여
[Django](%22https://www.djangoproject.com/%22)를 사용해서 사이트를 배포하는 과정을 설명한다.
여기서 로컬 컴퓨터는 Mac OS X 를 사용하였다. Django 앱을 실행시키기 위해서는 [Django
튜토리얼](%22https://docs.djangoproject.com/ko/2.2/intro/tutorial01/%22)을
참고하기 바란다.

#### Step 1. 패키지 업데이트 및 설치

Ubuntu에 연결을 하고 패키지들을 최신으로 업데이트한 후 패키지들을 설치한다.

    $ sudo apt-get update
    $ sudo apt-get dist-upgrade

#### Step 2. Z 쉘 설치

그리고 bash shell이 아니라 z shell을 사용하기 위해 zsh를 설치한 후 Oh My Zsh를 사용할 것이다.

    $ sudo apt-get install zsh
    $ sudo curl -L http://install.ohmyz.sh | sh

설치한 후 기본 zsh를 기본 쉘로 설정한 후 다시 시작한다. 그러면 앞에 `$` 대신 `~`로 나올것이다.

    $ sudo chsh ubuntu -s /usr/bin/zsh 

#### Step 3. Python 환경 설치

Ubuntu에는 Python 3.6이 설치되어 있다. 이제 Python 애플리케이션 개발을 위한 환경을 설치할 것이다.

    ~ sudo apt-get update 
    ~ sudo apt-get install python-dev python-setuptools

그리고 Python 패키지 설치를 위해 최신 버전의 `pip`를 설치한다.

    ~ sudo apt install python3-pip

마지막으로 가상환경을 설치해 자신이 원하는 패키지 등 개발을 위한 격리된 환경을 만들어 사용한다.

    ~ sudo apt-get install python3-venv

#### Step 4. 프로젝트를 위한 기본 세팅

이제 Django 앱 개발을 위해 `root`에 속하는 `srv` 폴더의 권한을 `ubuntu`로 전환 후 사용할 것이다.
`srv`폴더는 왭에 관련된 프로토콜을 위해 사용되는 데이터를 시스템에 두는 곳이라 생각하면 된다. 그리고 `srv` 폴더 안에
Django 앱을 프로젝트 폴더를 만든다.

    ~ sudo chown -R ubuntu:ubuntu /srv/
    
    # 폴더 생성
    ~ /srv
    ~ mkdir <프로젝트 이름>

#### Step 5. 프로젝트 이동

가상환경을 설치하기 전에 먼저 로컬 컴퓨터에서 작성한 Django 앱을 원격 서버인 Ubuntu 서버로 이동 시켜야 한다.
[Github](%22https://github.com/%22)을 사용하면 `git clone`을 사용하면 된다. 그 외에도 파일
이동 방법은 많지만 여기서는 `Secure Copy Protocol (scp)`를 사용할 것이다.  
먼저 로컬 컴퓨터에서 터미널을
    실행시킨다.

    $ scp -i <인증서위치> -r <프로젝트 폴더> ubuntu@<인스턴스 퍼블릭 DNS>:/srv/<프로젝트 폴더 이름>
    
    # 예시
    $ scp -i ~/.ssh/key.pem -r /Users/Projects/django_project/ ubuntu@ec2-123-456-789.ap-northeast-2.compute.amazonaws.com:/srv/django_project"

폴더가 아닌 파일을 이동할떄는 `-r` 없이 사용하면 된다.

#### Step 6. 가상환경 및 패키지 설치

이제 가상환경을 사용하여 Django 앱을 실행해보겠다. 먼저 프로젝트 폴더로 들어간다. 그리고 가상환경을 활성화 해서 필요한
Python 패키지들을 설치한다.

    ~ /srv/<프로젝트  폴더이름>
    
    # 폴더에 들어간 후
    python3 -m venv <가상환경이름>
    
    # 가상환경 활성화
    source <가상환경이름>/bin/activate

프로젝트에 필요한 패키지는 `requirements.txt`에 작성하거나 아니면 하나씩 설치하면된다. 만약
`requirements.txt`를 사용하는 경우 아래와 같이 실행시키면 된다.

    pip3 install -r requirements.txt

만약 간단한 Django 앱을 실행시킬 시 Django 패키지만 먼저 설치하고 추후 필요한 패키지는 직접 설치하면 된다.

    pip3 install Django==2.2.6

#### Step 7. Django 실행

마지막으로 AWS EC2 에서 Django 앱을 실행시키려면 아래 코드를 입력해야한다.

    python manage.py runserver 0:8080

이에 앞서 AWS EC2 Dashboard에 들어가서 EC2 생성할때 사용한 **Security Group**의
**Inbound**에 다음과 같이 추가하면 된다.

| Type       | Port Range |
| ---------- | ---------- |
| Custom TCP | 8080       |

### 마무리

이 문서는 AWS EC2 Ubuntu 서버를 사용하여 Django 앱을 설치하고 실행하는 방법에 대해서 배웠다. EC2에
데이터베이스를 설치해서 사용하는 과정은 [PostgreSQL
설치](https://github.com/whoareyouwhoami/ProjectCapulus/blob/master/README.md)를
참고하길 바란다. 다음에는 이 문서에서 작성한 Django 앱을 인터넷에 배포하는 방법에 대해서 알아보겠다.
