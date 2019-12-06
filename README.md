Project Tellus
================

### TEAM 11대0

데이터공학 프로젝트

> 목차

1.  Kickstater란?  
2.  [아키텍쳐]()  
3.  [서버 구성]()
      - [AWS Ubuntu EC2 와 Python Django](documentation/python_django.md)
      - [uWSGI, Nginx, AWS EC2 사용하여 Django
        배포](documentation/uwsgi_nginx.md)
4.  [데이터 전처리]()  
5.  [모델링 구성]()

## Kickstarter

Kickstarter는 투자자와 아이디어를 가진 창업자 또는 스타트업을 연결하는 소셜 펀딩 플랫폼이다. 인터넷을 통해 한 명 또는
소수의 투자자가 아닌, 수많은 사람으로부터 동시에 투자를 받을 수 있으며 투자에 성공한 아이디어 소유자는 투자한 사람들에게 약속된
보상을 제공하게 된다. Kickstarter는 이러한 소셜 펀딩 플랫폼 사이에서 가장 유명하다.

## 시스템 아키텍쳐

이번 프로젝트는 [Amazon Web Service](https://aws.amazon.com/ko/) 서비스를 사용하였다.
![시스템 아키텍쳐](documentation/figures/aws_arch.jpeg) AWS EC2 를 사용하여 왭 서버용
하나와 모델들을 돌려서 학습 시키는 서버를 사용했다. 그리고 모든 Amazon RDS를 사용해서 데이터 관리를 하였다.

### 사용중인 기술들

![왭 기술들](documentation/figures/used_soft.jpeg) ![모델
기술](documentation/figures/ml_soft.jpeg)

웹을 배포하기 위에 위에와 같이 Python, NGINIX, uWSGI, Django, PostgreSQL을 사용하였다. 그리고
유저의 요청을 받아서 해당 프로젝트의 성공률을 예측하는 방법으로는 Catboost와 Scikit-learn 안에 있는 기술들을
사용하였다.
