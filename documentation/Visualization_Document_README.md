
# Visualizing Data on Web
### 목표
사용자가 웹에 본인이 구상하고 있는 아이디어의 세부적인 수치를 입력하면 모델링의 결과로 성공/실패 확률을 보여주는 것 뿐만이 아니라, 더 나은 결정을 할 수 있도록 전체 데이터의 동향을 인터랙티브 시각화를 통해 알려주도록 한다.




### 데이터 출처
해당 프로젝트의 기본 데이터로 사용된 [kaggle의 kickstarter 데이터셋](https://www.kaggle.com/kemical/kickstarter-projects)뿐만이 아니라 주기적인 크롤링을 통해 DB에 쌓아둔 새로운 kickstarter project 정보까지 활용하여 시각화를 진행한다.




### 사용한 라이브러리
웹에서 사용자에게 보여줄 그래프를 그리기 위해 interactive한 그래프를 그려주는 plotly를 활용한다.



### About VisCls Class
VisCls Class는 시각화 함수 5개를 담고 있다.

1. g_success_term() : 카테고리와 목표 금액이 주어졌을 때 '기간별' 성공률을 확인할 수 있는 함수이다.
2. g_goal_dist() : 카테고리와 펀딩 기간이 주어졌을 때 목표 금액이 어떻게 분포되어있는지, 목표 금액별로 성공한 프로젝트와 실패한 프로젝트의 비율이 어떻게 되는지를 확인할 수 있는 함수이다.
3. g_pledge_pp() : 카테고리와 펀딩 기간이 주어졌을 때 후원자 1인당 투자 금액의 분포를 확인할 수 있는 함수이다.
4. g_success_cat_amount() : 카테고리와 목표 금액이 주어졌을 때 기간별로 성공률이 어떻게 되는지 확인한다.
5. g_success_by_curr() : 카테고리, 목표 금액, 기간이 주어졌을 때 어떤 화폐단위가 가장 성공률이 높은지를 확인할 수 있는 함수이다. 


