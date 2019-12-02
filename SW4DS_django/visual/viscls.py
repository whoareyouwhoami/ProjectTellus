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
                   'x': ['below 500', 'above 500~\nbelow 1000', 'above 1000~\nbelow 3000', 'above 3000~\nbelow 5000', 'above 5000~\nbelow 10000', 'above 10000~\nbelow 50000', 'above 50000~\nbelow 100000', 'above 100000'],
                   'y': percent_list}

        ################# 여기요 #################
        term_list = ['10 Days or less', 'above 10 Days and below 15 Days', 'above 15 Days and below 21 Days', 'above 21 Days and below 30 Days', 'above 30 Days and below 45 Days', 'above 45 Days and below 60 Days',
                     'above 60 Days and below 92 Days']
        title_main = "Rate of success for '"+ self.cate +"' when funding period is " + term_list[self.term_bin - 1]
        title = {'text': title_main}
        ########################################

        fig = go.Figure({"data": res_dct, "layout": {"title": title}})
        fig.update_traces(marker_color='#78BD40')
        fig.update_layout(font={'size':9})

        html_str = plot(fig, output_type='div', include_plotlyjs=False)
        return html_str


    def g_goal_dist(self):
        df = data.loc[(data['category'] == self.cate) & (data['term_bin'] == self.term_bin)]
        x_range = ['below 500', 'above 500~\nbelow 1000', 'above 1000~\nbelow 3000', 'above 3000~\nbelow 5000', 'above 5000~\nbelow 10000', 'above 10000~\nbelow 50000', 'above 50000~\nbelow 100000', 'above 100000']

        fin = df.groupby(['state', 'usd_goal_real_bin']).size().to_frame().unstack().fillna(0)
        fin.index.names = [None]
        fin = fin[0].T.reset_index()

        suc = go.Bar(name='success', x=x_range, y=fin['success'], marker_color='#1100FF')
        fail = go.Bar(name='failed', x=x_range, y=fin['failed'], marker_color='#FE0002')

        ################# 여기요 #################
        term_list = ['10 Days or less', 'above 10 Days and below 15 Days', 'above 15 Days and below 21 Days', 'above 21 Days and below 30 Days', 'above 30 Days and below 45 Days', 'above 45 Days and below 60 Days',
                     'above 60 Days and below 92 Days']
        title = "Number of projects for '"+ self.cate +"' when funding period is " + term_list[self.term_bin - 1]
        ########################################

        fig = go.Figure(data=[suc, fail])
        fig.update_layout(barmode='stack', title=title, font={'size':9})

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
                   'x': ['below 50', 'above 50~\nbelow 100', 'above 100~\nbelow 500', 'above 500~\nbelow 1000', 'above 1000~\nbelow 2500', 'above 2500~\nbelow 5000', 'above 5000'],
                   'y': percent_list}

        ################# 여기요 #################
        term_list = ['10 Days or less', 'above 10 Days and below 15 Days', 'above 15 Days and below 21 Days', 'above 21 Days and below 30 Days', 'above 30 Days and below 45 Days', 'above 45 Days and below 60 Days',
                     'above 60 Days and below 92 Days']
        title_main = "Average funding amount(USD) per person for '"+ self.cate +"' when funding period is " + term_list[self.term_bin - 1]
        title = {'text': title_main}
        ########################################

        fig = go.Figure({"data": res_dct, "layout": {"title": title}})
        fig.update_traces(marker_color='#78BD40')
        fig.update_layout(font={'size':9})

        html_str = plot(fig, output_type='div', include_plotlyjs=False)
        return html_str



