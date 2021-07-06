#!/usr/bin/env python3
# coding: utf-8

# # Get Data from SQL
# Set the weight of voting

import pandas as pd
import datetime
import json
import catboost as cb
import SW4DS_django.database.db as dbt


data = pd.DataFrame()
nlp_data = pd.DataFrame()


gd = pd.read_csv('ks-projects-201801.csv')


#data for all
# get state from DB and append to data DF
state = []

sql = "select state from ml.testcrawl2"
dbt.cur.execute(sql)
res = dbt.cur.fetchall()

for i in res:
    state.append(i['state'])
    
# state of only datas in db
state_db = state.copy()
    
# state including the state of gd
state.extend(gd['state'])
data['state'] = state.copy()


# binnarize the dependent variable
data['state_bin'] = data['state'].apply(lambda x: 1 if (x == 'success' or x == 'successful') else 0)


# data for NLP

gd_blurb = pd.read_csv('df_text_eng.csv')
gd_blurb['blurb'][0]


# get blurb from DB and append to data DF
blurb = []

sql = "select blurb from ml.testcrawl2"
dbt.cur.execute(sql)
res = dbt.cur.fetchall()

for i in res:
    blurb.append(i['blurb'])
    
# extend the blurb list by the gd_nlp
blurb.extend(gd_blurb['blurb'])
    
nlp_data['blurb'] = blurb


state_db.extend(gd_blurb['state'])

nlp_data['state'] = state_db.copy()
nlp_data['state_bin'] = nlp_data['state'].apply(lambda x: 1 if (x == 'success' or x == 'successful') else 0)


# # data for non-NLP


# get currency_type from DB
currency_type = []

sql = "select currency_type from ml.testcrawl2"
dbt.cur.execute(sql)
res = dbt.cur.fetchall()

for i in res:
    currency_type.append(i['currency_type'])
    
# currency_type including the currency_type of gd
currency_type.extend(gd['currency'])
    
data['currency'] = currency_type

# get cate from DB
category = []

sql = "select category from ml.testcrawl2"
dbt.cur.execute(sql)
res = dbt.cur.fetchall()

for i in res:
    category.append(i['category'])
    
# currency_type including the currency_type of gd
category.extend(gd['main_category'])
    
data['category'] = category



# get usd_goal_real from DB
usd_goal_real = []

sql = "select usd_goal_real from ml.testcrawl2"
dbt.cur.execute(sql)
res = dbt.cur.fetchall()

for i in res:
    usd_goal_real.append(i['usd_goal_real'])
    
# adding the gd info
usd_goal_real.extend(gd['usd_goal_real'])
    
data['usd_goal_real'] = usd_goal_real

# get launched data from DB
launched = []

sql = "select launched from ml.testcrawl2"
dbt.cur.execute(sql)
res = dbt.cur.fetchall()

for i in res:
    launched.append(i['launched'])

# adding the gd info
launched.extend(gd['launched'])
    
data['launched'] = launched


# get deadline data from DB
deadline = []

sql = "select deadline from ml.testcrawl2"
dbt.cur.execute(sql)
res = dbt.cur.fetchall()

for i in res:
    deadline.append(i['deadline'])
    
# adding the gd info
deadline.extend(gd['deadline'])
    
data['deadline'] = deadline




# get country data from DB
country = []

sql = "select country from ml.testcrawl2"
dbt.cur.execute(sql)
res = dbt.cur.fetchall()

for i in res:
    country.append(i['country'])

# adding the gd country
country.extend(gd['country'])
    
data['country'] = country

# country name unification
data['country'] = data['country'].apply(lambda x: 'Canada' if (x == 'CA') else x )
data['country'] = data['country'].apply(lambda x: 'Australia' if x == 'AU' else x )
data['country'] = data['country'].apply(lambda x: 'Germany' if x == 'DE' else x )
data['country'] = data['country'].apply(lambda x: 'France' if x == 'FR' else x)
data['country'] = data['country'].apply(lambda x: 'Italy' if x == 'IT' else x)
data['country'] = data['country'].apply(lambda x: 'Netherlands' if x == 'NL' else x)
data['country'] = data['country'].apply(lambda x: 'Spain' if x == 'ES' else x)
data['country'] = data['country'].apply(lambda x: 'Singapore' if x == 'SG' else x)
data['country'] = data['country'].apply(lambda x: 'UK' if x == 'GB' else x)
data['country'] = data['country'].apply(lambda x: 'US' if x == 'Los Angeles' else x)


# # Extracting the right info from pd
projects = data[data['country']!=''].copy()

projects['launched_year'] = projects.apply(lambda x: x['launched'].split(" ")[0].split("-")[0], axis = 1)
projects['launched_month'] = projects.apply(lambda x: x['launched'].split(" ")[0].split("-")[1], axis = 1)
projects['launched_day'] = projects.apply(lambda x: x['launched'].split(" ")[0].split("-")[2], axis = 1)
projects['launched_date'] = projects.apply(lambda x: x['launched'].split(" ")[0].split("-")[1] + x['launched'].split(" ")[0].split("-")[2], axis = 1)

projects['deadline_dt'] = projects.apply(lambda x: datetime.datetime.strptime(x['deadline'], "%Y-%m-%d").date(), axis = 1)
projects['launched_dt'] = projects.apply(lambda x: datetime.datetime.strptime(x['launched'].split(" ")[0], "%Y-%m-%d").date(), axis = 1)

projects['term'] = projects.apply(lambda x: int(str(x['deadline_dt'] - x['launched_dt']).split(" ")[0]), axis = 1)
projects['term_str'] = projects.apply(lambda x: str(x['term']), axis = 1)


# 중도 취소로 인해 term이 왜곡된 row 삭제
projects = projects[lambda x: x['term'] > 1]


# launch 날짜가 1970년으로 되어있는 row는 삭제
projects_new = projects[lambda x: x['term'] < 100]

projects_new = projects_new.reset_index().drop(['index'], axis = 1)


projects_new['term_str'] = projects_new.apply(lambda x: x['term_str'] if len(x['term_str']) != 1
                                             else '0' + x['term_str'], axis = 1)


# 10만원 이하로 펀딩 받는 경우는 지움
projects_new = projects_new[projects_new['usd_goal_real'] > 100]


projects_new = projects_new[projects_new['country'].isin(['US', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Italy', 'Netherlands', 'Spain', 'Singapore'])]


projects_fin = projects_new[projects_new['currency'].isin(['USD', 'GBP', 'EUR', 'CAD', 'AUD', 'SGD'])]


# # Processing the Data into a Trainable data


# Creating the dataset
train_data = projects_fin[['category', 'currency', 'country', 'usd_goal_real', 'state_bin', 'launched_year', 'launched_month', 'term']].copy()

train = pd.DataFrame()

# Assigning a categorical type to categorical varibles and vectorizing the categories for simplification
train['main_category'] = train_data['category'].astype('category').cat.codes
train['currency'] = train_data['currency'].astype('category').cat.codes
train['country'] = train_data['country'].astype('category').cat.codes

# export labes for vectorizing

main_c = train_data['category'].astype('category')
curre_c = train_data['currency'].astype('category')
count_c = train_data['country'].astype('category')
main_d = dict(enumerate(main_c.cat.categories))
curre_d = dict(enumerate(curre_c.cat.categories))
count_d = dict(enumerate(count_c.cat.categories))

main = {y:x for x,y in main_d.items()}
curre = {y:x for x,y in curre_d.items()}
count = {y:x for x,y in count_d.items()}

cat_labels = {'main_category' : main, 'currency' : curre, 'country': count}
cat_json = json.dumps(cat_labels)
f = open("cat_labels.json","w")
f.write(cat_json)
f.close()

train[['usd_goal_real', 'launched_year', 'launched_month', 'term', 'state']] = train_data[['usd_goal_real', 'launched_year', 'launched_month', 'term', 'state_bin']]


train['launched_year'] = (train['launched_year']).astype('int')
train['launched_month'] = (train['launched_month']).astype('int')


cb_clf = cb.CatBoostClassifier(task_type = 'CPU')


# Labelling the categorical features
cat_features= [0,1,2]

# define train set
x = train.iloc[:,:-1]
y = train.iloc[:,-1]

# train model
cb_clf.fit(x, y, cat_features)


import pickle

filename = 'Non_nlp_model' # name to store model
pickle.dump(cb_clf, open(filename, 'wb')) # pickling


import re

def clean(text):
    text = str(text)
    text = re.findall(r'\w+', text)
    return ' '.join(text)

nlp_data['blurb'] = nlp_data['blurb'].apply(lambda x: clean(x))



from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer().fit(nlp_data['blurb'])
x = vectorizer.transform(nlp_data['blurb'])

filename = 'vectorizer.sav'
pickle.dump(vectorizer, open(filename, 'wb'))



from sklearn.linear_model import LogisticRegression

sgd = LogisticRegression()



sgd.fit(x, nlp_data['state_bin'])


# In[192]:


filename = 'NLP_model.sav'
pickle.dump(sgd, open(filename, 'wb'))

