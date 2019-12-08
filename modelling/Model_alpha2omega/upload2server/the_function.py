import json
import pickle
import datetime
import pandas as pd


# load model
cb_clf = pickle.load(open('Non_nlp_model', 'rb'))
lg_clf = pickle.load(open('nlp_model.sav', 'rb'))


# Assuming that the input from the Web is sent as a dict format
# a function that preprocess the input
def preprocess_nnlp(project):
    # turn the input into adequate variables
    project['launched_year'] = project.apply(lambda x: x['launched'].split(" ")[0].split("-")[0], axis = 1)
    project['launched_month'] = project.apply(lambda x: x['launched'].split(" ")[0].split("-")[1], axis = 1)
    project['launched_day'] = project.apply(lambda x: x['launched'].split(" ")[0].split("-")[2], axis = 1)
    project['launched_date'] = project.apply(lambda x: x['launched'].split(" ")[0].split("-")[1] + x['launched'].split(" ")[0].split("-")[2], axis = 1)
    project['deadline_dt'] = project.apply(lambda x: datetime.datetime.strptime(x['deadline'], "%Y-%m-%d").date(), axis = 1)
    project['launched_dt'] = project.apply(lambda x: datetime.datetime.strptime(x['launched'].split(" ")[0], "%Y-%m-%d").date(), axis = 1)
    project['term'] = project.apply(lambda x: int(str(x['deadline_dt'] - x['launched_dt']).split(" ")[0]), axis = 1)
    project['term_str'] = project.apply(lambda x: str(x['term']), axis = 1)
    
    #select required columns
    train_data = project[['main_category', 'currency', 'country', 'usd_goal_real', 'launched_year', 'launched_month', 'term', 'blurb']]
    
    # Assigning a categorical type to categorical varibles and vectorizing the categories for simplification
    with open('cat_labels.json') as json_file:
        data = json.load(json_file)
    
    train = pd.DataFrame()
    
    train['main_category'] = train_data['main_category'].map(data['main_category'])
    train['currency'] = train_data['currency'].map(data['currency'])
    train['country'] = train_data['country'].map(data['country'])
    
    # get the remaing variables
    train[['usd_goal_real', 'launched_year', 'launched_month', 'term']] = train_data[['usd_goal_real', 'launched_year', 'launched_month', 'term']]
    
    # turn categories into integer
    train['main_category'] = train['main_category'].astype('int8')
    train['currency'] = train['currency'].astype('int8')
    train['country'] = train['country'].astype('int8')
    
    # turning into right variables
    train['launched_year'] = (train['launched_year']).astype('int')
    train['launched_month'] = (train['launched_month']).astype('int')
    
    return train


# In[17]:


def preprocess_nlp(project):
    # import vectorizer
    vectorizer = pickle.load(open('vectorizer.sav', 'rb'))
    
    return vectorizer.transform(project['blurb'])


# # The function that retuns the probability

# Assuming that the input from the Web is sent as a dict format

def the_function(iw):
    # predict
    nnlp_pred = cb_clf.predict_proba(preprocess_nnlp(iw))
    nlp_pred = lg_clf.predict_proba(preprocess_nlp(iw))

    # final probability
    return (nnlp_pred + nlp_pred)[0,1] / 2

