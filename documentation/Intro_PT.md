
# Welcome to KickHelpers.com


# 프로젝트 소개


### 역할분담


|  팀원  | 중간고사 이전                  | 중간고사 이후 |
| :----: | ------------------------------ | ------------- |
| 박지원 | Preprocessing                  | Modeling과 Front-end |
| 윤정하 | 자료 조사                      | Modeling |
| 정희영 | Modeling                      | Front-end와 Server |
| 주용우 | 웹사이트 개발을 위한 서버 작업 | Modeling과 Back-end |


### 일정

![](figure/schedule.jpg)

### 제품소개

<br>

  **KickHelpers란?** 
  
  - 최신 머신러닝 기법을 적용하여 간단한 몇가지 정보 입력만으로 크라우드 펀딩의 성공률을 예측해주는 서비스

  - 성공률이 높은 모금 전략을 세울 수 있는 맞춤형 그래프를 제공 (장소, 기간, 모금액 등)

<br>
  
  **[핵심가치]**
  
  - 창업자의 크라우드 펀딩 이용에 대한 막연함과 실패에 대한 두려움을 완화
  
  -> 창업 활성화를 통한 창의적이고 개방적인 사회에 기여


### 사용데이터

<br>

  크라우드펀딩 사이트 Kickstarter 데이터 (2005 ~ 현재까지, 한달에 한번 최신데이터 UPDATE)

### 대상고객

<br>
  
  - 크라우드 펀딩을 통해 창업하고자 하는 창업자 
  
  - 제품 아이디어만을 갖고 있는 일반인 (흥미 유발)  


### 예상수익과 사업확대전략

<br>

  - 웹사이트내 광고배너
  
  
  - Kickstarter 데이터 분석을 통한 컨설팅 -> 정보 제공 단계별 유료화 

      eg. 하위 단계: 해당 카테고리 분석 서비스 ~ 상위 단계: Start to End Service 
  
  
  - 입력받은 정보 가공 후 판매 
  
      eg. 향후 인기 분야 예상
      


```python
import pandas as pd
import numpy as np
pd.set_option('max_columns',999)
pd.set_option('max_rows',200)

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import seaborn as sns
sns.set() 
%matplotlib inline 
%config InlineBackend.figure_format = 'retina' 
sns.set_style(style='white')
sns.set_context(context ='paper')

import datetime
import os
from functools import reduce

# 한글 폰트 사용
plt.rcParams["font.family"] = 'NanumGothic'

df=pd.read_csv('data/projects_fin.csv')

df['launched'] =  pd.to_datetime(df['launched'])
df['Year'] =df['launched'].dt.strftime('%Y')
df['month'] =df['launched'].dt.strftime('%m')

cat_count=df.pivot_table(index='Year',columns='main_category',aggfunc='size')
cat_count=cat_count[cat_count.index!='2018']
top_n = 5
pd.DataFrame({col: cat_count.T[col].nlargest(top_n).index.tolist() 
                  for n, col in enumerate(cat_count.T)}).T

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2009</th>
      <td>Film &amp; Video</td>
      <td>Music</td>
      <td>Art</td>
      <td>Publishing</td>
      <td>Photography</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>Film &amp; Video</td>
      <td>Music</td>
      <td>Art</td>
      <td>Publishing</td>
      <td>Theater</td>
    </tr>
    <tr>
      <th>2011</th>
      <td>Film &amp; Video</td>
      <td>Music</td>
      <td>Art</td>
      <td>Publishing</td>
      <td>Theater</td>
    </tr>
    <tr>
      <th>2012</th>
      <td>Film &amp; Video</td>
      <td>Music</td>
      <td>Publishing</td>
      <td>Art</td>
      <td>Games</td>
    </tr>
    <tr>
      <th>2013</th>
      <td>Film &amp; Video</td>
      <td>Music</td>
      <td>Publishing</td>
      <td>Games</td>
      <td>Art</td>
    </tr>
    <tr>
      <th>2014</th>
      <td>Film &amp; Video</td>
      <td>Music</td>
      <td>Publishing</td>
      <td>Technology</td>
      <td>Games</td>
    </tr>
    <tr>
      <th>2015</th>
      <td>Film &amp; Video</td>
      <td>Technology</td>
      <td>Music</td>
      <td>Publishing</td>
      <td>Games</td>
    </tr>
    <tr>
      <th>2016</th>
      <td>Technology</td>
      <td>Film &amp; Video</td>
      <td>Games</td>
      <td>Design</td>
      <td>Music</td>
    </tr>
    <tr>
      <th>2017</th>
      <td>Games</td>
      <td>Technology</td>
      <td>Design</td>
      <td>Film &amp; Video</td>
      <td>Publishing</td>
    </tr>
  </tbody>
</table>
</div>



최근들어 Game, Technology, Design 카테고리가 뜨고 있고 

Film&Video, Music, Puvlishing, Art 카테고리가 상대적으로 밀리고 있다. 

이를 통해 크라우드 펀딩이 세계적 트렌드를 크게 반영하고 있음을 알 수 있다. 

(* 세계의 트렌드를 한국이 온전히 흡수하는데 1~2년 걸리는 것을 감안하면 
위와 같은 분석을 통해 한국의 단기 트렌드를 전망해 볼수도 있을 것이라 보여진다.)

  - 타기업 판매 (크라우드 펀딩 기업)
