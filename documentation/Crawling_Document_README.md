
# Updating data - Kicktraq Web Crawling
이 문서는 분석에 필요한 데이터를 주기적으로 업데이트하여 DB에 쌓기 위한 크롤링 작업을 수행하는 과정을 담고 있다.



### 크롤링 목표
kickstarter에 올라오는 최신 프로젝트 데이터를 주기적으로 받아와 모델링에 필요한 데이터를 업데이트 하여 더 정확한 예측을 가능하게 한다.




### 크롤링 데이터 출처
https://www.kicktraq.com/ --> kickstarter 홈페이지에 올라오는 프로젝트 정보를 동일하게 제공하는 'kicktraq' 홈페이지에서 데이터를 크롤링한다.




### 프로젝트를 크롤링 할 카테고리
kicktraq 홈페이지의 여러 카테고리 중에서 정보를 받아올 때는 아래에 해당하는 2개의 카테고리에서 각각 성공한 프로젝트와 실패한 프로젝트를 크롤링 해올 것이다.

[[성공한 프로젝트]] --> Day-1 Projects

[[실패한 프로젝트]] --> Archived Projects




### 사용한 라이브러리
본 프로젝트에서 크롤링 작업 수행 시 활용한 라이브러리는 Python의 Selenium이다.




### Structure
이 작업을 수행하기 위해 아래와 같은 이름의 4가지의 클래스를 구성하였고, 각 클래스의 역할과 그 안에 속한 함수들은 아래와 같다. <br>
**1. KicktraqOpen** : Kicktraq 홈페이지를 Chrome driver를 통해 연다. <br>
**2. WebcrawlClean** : Kicktraq에서 받아올 정보를 전처리한다. <br>
**3. KicktraqPage** : Kicktraq에서 정보를 받아온다. <br>
**4. KicktraqCrawl** : Kicktraq 홈페이지에서 정보를 받아오기 위해 Chrome driver를 제어한다. <br>  

![class_function](https://user-images.githubusercontent.com/31986977/70239782-4bffea80-17af-11ea-940b-f1209c6c4ef9.png)



### Data

받아와야 할 프로젝트의 세부 정보는 다음과 같다.

- name : 이름
- blurb : 한 줄 설명
- state : 상태 (목표치 이상으로 펀딩 받으면 성공, 아니면 실패)
- category : 메인 카테고리
- funding_rate : 펀딩 받은 금액의 비율 (pledged / goal * 100)
- pledged : 펀딩 받은 금액
- goal : 펀딩 목표 금액
- launched : 펀딩 시작 날짜
- deadline : 펀딩 끝난 날짜
- country : 프로젝트 시작 국가

위의 정보가 담겨있는 element의 xpath를 통해 데이터를 받아온다.




### 의의
'최신 데이터를 지속적으로 받아와 DB에 저장'하기 때문에 기존에 서비스 개발을 위해 사용한 기초 데이터 이외에도 새로운 데이터를 활용할 수 있어 시간이 지나도 분석력이 높은 모델을 구축할 수 있다.
