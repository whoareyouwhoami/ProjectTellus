
# Preprocessing & Explore data
이 문서는 분석에 필요한 데이터를 분석에 사용할 수 있도록 전처리하고 EDA하는 과정을 담고 있다.

### 목표
모델의 예측력을 높이기 위해 새로운 feature를 설정하고 불필요한 row를 제거한다.




### 데이터 출처
해당 프로젝트의 기본 데이터는 [kaggle의 kickstarter 데이터셋](https://www.kaggle.com/kemical/kickstarter-projects)으로부터 시작되었음을 밝힌다.




### 전처리 세부 내용
[새로운 컬럼 추가]
- state_new : usd_pledged_real이 usd_goal_real 이상이면 (즉, 모금 받은 금액이 목표 금액 이상이면) success, 미만이면 failed로 state 재정의
- deadline_dt / launched_dt : deadline과 launched 날짜를 datetime type으로 변환한 것. 연-월-일 구조로 되어있음
- term : deadline_dt와 launched_dt 날짜 사이의 간격
- term_str : term은 int type. 이를 string type으로 바꾼 것
- term_bin : term 컬럼 값 binning. string type
- usd_goal_real_bin : usd_goal_real 컬럼 값 binning. string type

[불필요한 row 제거]
- 모금 기간이 100일 초과하는 경우(약 14000일 정도 됨)는 지움. 모금 시작 날짜가 1970년으로 되어있다.
- usd_goal_real의 값이 100 이하인 경우는 지움. 약 10만원 이하로 펀딩을 받는 것은 무의미하다고 생각했기 때문이다.




### 사용한 라이브러리
본 프로젝트에서 전처리 및 EDA 작업 수행 시 활용한 라이브러리는 Python의 pandas와 matplotlib / seaborn이다.
