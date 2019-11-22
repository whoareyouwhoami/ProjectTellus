AWS Ubuntu EC2 + Python Django
================

### AWS EC2 사용하여 Django 앱 배포

이 문서는 AWS EC2 Ubuntu 18.04 LTS를 사용하여 Django를 사용해서 사이트를 배포하는 과정을 설명한다.

<br>

#### Step 1

Ubuntu에 연결을 하고 패키지들을 최신으로 업데이트한 후 패키지들을 설치한다.

    $ sudo apt-get update
    $ sudo apt-get dist-upgrade

#### Step 2

그리고 bash shell이 아니라 z shell을 사용하기 위해 zsh를 설치한 후 Oh My Zsh를 사용할 것이다.

    $ sudo apt-get install zsh
    $ sudo curl -L http://install.ohmyz.sh | sh

설치한 후 기본 zsh를 기본 쉘로 설정한 후 다시 시작한다. 그러면 앞에 `$` 대신 `~`로 나올것이다.

    $ sudo chsh ubuntu -s /usr/bin/zsh 

#### Step 3

Ubuntu에는 Python 3.6이 설치되어 있다. 이제 Python 애플리케이션 개발을 위한 환경을 설치할 것이다.

    ~ sudo apt-get update 
    ~ sudo apt-get install python-dev python-setuptools

그리고 Python 패키지 설치를 위해 최신 버전의 `pip`를 설치한다.

    ~ sudo apt install python3-pip

마지막으로 가상환경을 설치해 자신이 원하는 패키지 등 개발을 위한 격리된 환경을 만들어 사용한다.

    ~ sudo apt-get install python3-venv

#### Step 4

이제 Django 앱 개발을 위해 `root`에 속하는 `srv` 폴더의 권한을 `ubuntu`로 전환 후 사용할 것이다.
`srv`폴더는 왭에 관련된 프로토콜을 위해 사용되는 데이터를 시스템에 두는 곳이라 생각하면 된다. 그리고 `srv` 폴더 안에
Django 앱을 프로젝트 폴더를 만든다.

    ~ sudo chown -R ubuntu:ubuntu /srv/
    
    # 폴더 생성
    ~ /srv
    ~ mkdir <프로젝트 이름>

#### Step 5

가상환경을 설치하기 전에 먼저 로컬 컴퓨터에서 작성한 Django 앱을 원격 서버인 Ubuntu 서버로 이동 시켜야 한다.
[Github](%22https://github.com/%22)을 사용하면 `git clone`을 사용하면 된다. 그 외에도 파일
이동 방법은 많지만 여기서는 `Secure Copy Protocol (scp)`를 사용할 것이다.

    scp -i <인증서위치> -r <프로젝트 폴더> ubuntu@<인스턴스 퍼블릭 DNS>:/srv/<프로젝트 이름>
    
    # 예시
    scp -i ~/.ssh/key.pem -r /Users/Projects/django_project/ ubuntu@ec2-123-456-789.ap-northeast-2.compute.amazonaws.com:/srv/django_project"

폴더가 아닌 파일을 이동할떄는 `-r` 없이 사용하면 된다.
