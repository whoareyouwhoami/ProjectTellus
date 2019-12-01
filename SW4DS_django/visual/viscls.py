import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

import database.db as dbt
import required.data as reqdata


pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

##############################
# Visual
##############################

sql_call = dbt.DBcls.sqlselectALL()
db_data = pd.DataFrame(sql_call)

projects_fin = reqdata.data_fin
temp_data = projects_fin[
            ['name', 'state_new', 'main_category', 'deadline', 'launched', 'usd_pledged_real', 'usd_goal_real', 'term',
             'term_bin', 'usd_goal_real_bin', 'backers']].copy()

temp_data.rename(columns={'main_category': 'category', 'state_new': 'state'}, inplace=True)

data = pd.concat([db_data, temp_data], sort=False)


class VisCls():
    def __init__(self, cate, term_bin):
        self.cate = cate
        self.term_bin = term_bin

    def g_success_term(self):
        df = data.loc[(data['category'] == self.cate) & (data['term_bin'] == self.term_bin)]
        percent_list = []

        for i in range(1, 9):
            numerator = len(df.loc[(df['usd_goal_real_bin'] == i) & (df['state'] == 'success')])
            denominator = len(df.loc[df['usd_goal_real_bin'] == i])
            print("Numerator:", numerator, "Denominator:", denominator)

            if denominator == 0:
                percent = 0
            else:
                percent = round(((numerator / denominator) * 100), 2)
            percent_list.append(percent)

        res_dct = {'type': 'bar',
                   'x': ['500달러이하', '1000달러이하', '3000달러이하', '5000달러이하', '10000달러이하', '50000달러이하', '100000이하', '100000초과'],
                   'y': percent_list}

        ################# 여기요 #################
        term_list = ['10일 이하', '10일 초과 15일 이하', '15일 초과 21일 이하', '21일 초과 30일 이하', '30일 초과 45일 이하', '45일 초과 60일 이하',
                     '60일 초과 92일 이하']
        title_main = term_list[self.term_bin - 1] + ' 기간일 때 ' + self.cate + ' 카테고리의 금액별 성공률'
        title = {'text': title_main}
        ########################################

        fig = go.Figure({"data": res_dct, "layout": {"title": title}})
        fig.update_traces(marker_color='#78BD40')
        html_str = plot(fig, output_type='div', include_plotlyjs=False)
        return html_str


    def g_goal_dist(self):
        df = data.loc[(data['category'] == self.cate) & (data['term_bin'] == self.term_bin)]
        x_range = ['500달러이하', '1000달러이하', '3000달러이하', '5000달러이하', '10000달러이하', '50000달러이하', '100000이하', '100000초과']

        fin = df.groupby(['state', 'usd_goal_real_bin']).size().to_frame().unstack().fillna(0)
        fin.index.names = [None]
        fin = fin[0].T.reset_index()

        suc = go.Bar(name='success', x=x_range, y=fin['success'], marker_color='#1100FF')
        fail = go.Bar(name='failed', x=x_range, y=fin['failed'], marker_color='#FE0002')

        ################# 여기요 #################
        term_list = ['10일 이하', '10일 초과 15일 이하', '15일 초과 21일 이하', '21일 초과 30일 이하', '30일 초과 45일 이하', '45일 초과 60일 이하',
                     '60일 초과 92일 이하']
        title = term_list[self.term_bin - 1] + ' 기간일 때 ' + self.cate + ' 카테고리의 목표 금액 분포'
        ########################################

        fig = go.Figure(data=[suc, fail])
        fig.update_layout(barmode='stack', title=title)

        html_str = plot(fig, output_type='div', include_plotlyjs=False)
        return html_str


    def g_pledge_pp(self):

        df_call = data.loc[(data['category'] == self.cate) & (data['term_bin'] == self.term_bin)]
        df = df_call.loc[df_call['backers'] != 0]
        df = df.copy()
        df['pledge_per_person'] = df['usd_goal_real'] / df['backers']
        df['pledge_per_person_bin'] = df.apply(lambda x: '1' if x['pledge_per_person'] <= 50 else '2' if x['pledge_per_person'] <= 100 else '3' if x['pledge_per_person'] <= 500 else '4' if x['pledge_per_person'] <= 1000 else '5' if x['pledge_per_person'] <= 2500 else '6' if x['pledge_per_person'] <= 5000 else '7', axis=1)

        percent_list = []

        for i in range(7):
            sval = str(i + 1)
            numerator = len(df.loc[df['pledge_per_person_bin'] == sval])
            denominator = len(df)
            print("Numerator:", numerator, "Denominator:", denominator)
            if denominator == 0:
                percent = 0
            else:
                percent = round(((numerator / denominator) * 100), 2)

            percent_list.append(percent)

        res_dct = {'type': 'bar',
                   'x': ['50달러이하', '100달러이하', '500달러이하', '1000달러이하', '2500달러이하', '5000달러이하', '5000달러초과'],
                   'y': percent_list}

        ################# 여기요 #################
        term_list = ['10일 이하', '10일 초과 15일 이하', '15일 초과 21일 이하', '21일 초과 30일 이하', '30일 초과 45일 이하', '45일 초과 60일 이하',
                     '60일 초과 92일 이하']
        title_main = term_list[self.term_bin - 1] + ' 기간일 때 ' + self.cate + ' 카테고리의 1인당 투자 금액 분포'
        title = {'text': title_main}
        ########################################

        fig = go.Figure({"data": res_dct, "layout": {"title": title}})
        fig.update_traces(marker_color='#78BD40')

        html_str = plot(fig, output_type='div', include_plotlyjs=False)
        return html_str



