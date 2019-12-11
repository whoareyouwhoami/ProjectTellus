import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

import database.db as dbt
import required.data as reqdata

##############################
# Visual
##############################2

sql_call = dbt.DBcls.sqlselectALL()
db_data = pd.DataFrame(sql_call)

projects_fin = reqdata.data_fin
temp_data = projects_fin[
            ['name', 'state_new', 'main_category', 'deadline', 'launched', 'usd_pledged_real', 'usd_goal_real', 'term',
             'term_bin', 'usd_goal_real_bin', 'backers', 'currency']].copy()

temp_data.rename(columns={'main_category': 'category', 'state_new': 'state'}, inplace=True)

data = pd.concat([db_data, temp_data], sort=False)


class VisCls():
    def __init__(self, cate, term_bin, usd_goal_real_bin):
        self.cate = cate
        self.term_bin = term_bin
        self.usd_goal_real_bin = usd_goal_real_bin

    def g_success_term(self):
        df = data.loc[(data['category'] == self.cate) & (data['term_bin'] == self.term_bin)]
        percent_list = []

        for i in range(1, 9):
            numerator = len(df.loc[(df['usd_goal_real_bin'] == i) & (df['state'] == 'success')])
            denominator = len(df.loc[df['usd_goal_real_bin'] == i])

            if denominator == 0:
                percent = 0
            else:
                percent = round(((numerator / denominator)), 2)
            percent_list.append(percent)

        ####################
        # DATA
        ####################
        res_dct = {'type': 'bar',
                   'x': ['below 500', 'above 500~<br>below 1000', 'above 1000~<br>below 3000', 'above 3000~<br>below 5000', 'above 5000~<br>below 10000', 'above 10000~<br>below 50000', 'above 50000~<br>below 100000', 'above 100000'],
                   'y': percent_list}

        ####################
        # LABELS
        ####################
        term_list = ['10 days or less', 'above 10 days and below 15 days', 'above 15 days and below 21 days', 'above 21 days and below 30 days', 'above 30 days and below 45 days', 'above 45 days and below 60 days',
                     'above 60 days']
        title_main = "Rate of success for '"+ self.cate +"'<br> when funding period is " + term_list[self.term_bin - 1]
        title = {'text': title_main}

        ####################
        # GRAPH
        ####################
        fig = go.Figure({"data": res_dct, "layout": {"title": title}})

        fig.update_traces(marker_color='#78BD40')
        fig.update_layout(title_x=0.5, yaxis=dict(tickformat="%"), xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Goal amount(USD)")), font={'size': 9})

        html_str = plot(fig, output_type='div', include_plotlyjs=False)
        return html_str


    def g_goal_dist(self):
        df = data.loc[(data['category'] == self.cate) & (data['term_bin'] == self.term_bin)]
        x_range = ['below 500', 'above 500~<br>below 1000', 'above 1000~<br>below 3000', 'above 3000~<br>below 5000', 'above 5000~<br>below 10000', 'above 10000~<br>below 50000', 'above 50000~<br>below 100000', 'above 100000']

        fin = df.groupby(['state', 'usd_goal_real_bin']).size().to_frame().unstack().fillna(0)
        fin.index.names = [None]
        fin = fin[0].T.reset_index()

        ####################
        # DATA
        ####################
        suc = go.Bar(name='success', x=x_range, y=fin['success'], marker_color='#1100FF')
        fail = go.Bar(name='failed', x=x_range, y=fin['failed'], marker_color='#FE0002')

        ####################
        # LABELS
        ####################
        term_list = ['10 days or less', 'above 10 days and below 15 days', 'above 15 days and below 21 days', 'above 21 days and below 30 days', 'above 30 days and below 45 days', 'above 45 days and below 60 days',
                     'above 60 days']
        title = "Number of projects for '"+ self.cate +"'<br> when funding period is " + term_list[self.term_bin - 1]

        ####################
        # GRAPH
        ####################
        fig = go.Figure(data=[suc, fail])

        fig.update_layout(barmode='stack', title={'text': title}, title_x=0.5, font={'size': 9}, xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Goal amount(USD)")))

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

            if denominator == 0:
                percent = 0
            else:
                percent = round(((numerator / denominator)), 2)

            percent_list.append(percent)

        ####################
        # DATA
        ####################
        res_dct = {'type': 'bar',
                   'x': ['below 50', 'above 50~<br>below 100', 'above 100~<br>below 500', 'above 500~<br>below 1000', 'above 1000~<br>below 2500', 'above 2500~<br>below 5000', 'above 5000'],
                   'y': percent_list}

        ####################
        # LABELS
        ####################
        term_list = ['10 days or less', 'above 10 days and below 15 days', 'above 15 days and below 21 days', 'above 21 days and below 30 days', 'above 30 days and below 45 days', 'above 45 days and below 60 days',
                     'above 60 days']
        title_main = "Distribution for '"+ self.cate +"'<br> when funding period is " + term_list[self.term_bin - 1]
        title = {'text': title_main}

        ####################
        # GRAPH
        ####################
        fig = go.Figure({"data": res_dct, "layout": {"title": title}})

        fig.update_traces(marker_color='#78BD40')
        fig.update_layout(title_x=0.5, xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Average funding amount(USD) per person")), yaxis=dict(tickformat="%"), font={'size': 9})

        html_str = plot(fig, output_type='div', include_plotlyjs=False)
        return html_str


    def g_success_cat_amount(self):
        ########################################################################
        # 카테고리와 목표 금액이 주어졌을 때 기간별로 성공률이 어떻게 되는지 확인한다.
        ########################################################################
        cate_df = data[lambda x: (x['category'] == self.cate) & (x['usd_goal_real_bin'] == self.usd_goal_real_bin)]

        percent_list = []

        # 각 기간별 성공률 확인
        for i in range(1, 9):
            numerator = len(cate_df[lambda x: (x['term_bin'] == i) & (x['state'] == 'success')])
            denominator = len(cate_df[lambda x: x['term_bin'] == i])

            if denominator == 0:
                percent = 0
            else:
                percent = round(((numerator / denominator)), 2)

            percent_list.append(percent)

        ####################
        # DATA
        ####################
        # x축은 기간, y축은 성공률
        res_dct = {'type': 'bar',
        'x': ['10 days or less', 'above 10 days~<br> below 15 days', 'above 15 days~<br> below 21 days', 'above 21 days~<br> below 30 days', 'above 30 days~<br> below 45 days', 'above 45 days~<br> below 60 days',
        'above 60 days'],
        'y': percent_list}

        ####################
        # LABELS
        ####################
        goal_list = ['below $500', 'above $500 ~ below $1000', 'above $1000 ~ below $3000', 'above $3000 ~ below $5000', 'above $5000 ~ below $10000',
        'above $10000 ~ below $50000', 'above $50000 ~ below $100000', 'above $100000']
        title_main = "Rate of success for '"+ self.cate +"'<br> when funding goal is " + goal_list[self.usd_goal_real_bin - 1]
        title = {'text': title_main}

        ####################
        # GRAPH
        ####################
        fig = go.Figure({"data": res_dct, "layout": {"title": title}})

        fig.update_traces(marker_color='#78BD40')
        fig.update_layout(title_x=0.5, xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Funding period")),yaxis=dict(tickformat="%"),font={'size':9})

        html_str = plot(fig, output_type='div', include_plotlyjs=False)
        return html_str

    def g_success_by_curr(self):
        # 카테고리, 목표 금액, 기간이 주어졌을 때 어떤 화폐단위가 가장 성공률이 높은가

        cate_df = data[
            lambda x: (x['category'] == self.cate) & (x['usd_goal_real_bin'] == self.usd_goal_real_bin) & (
                        x['term_bin'] == self.term_bin)]
        curr_list = ['AUD', 'CAD', 'EUR', 'GBP', 'SGD', 'USD']
        percent_list = []

        for i in curr_list:
            numerator = len(cate_df[lambda x: (x['currency'] == i) & (x['state'] == 'success')])
            denominator = len(cate_df[lambda x: x['currency'] == i])

            if denominator == 0:
                percent = 0
            else:
                percent = round(((numerator / denominator)), 2)
            percent_list.append(percent)

        ####################
        # DATA
        ####################
        res_dct = {'type': 'bar',
                   'x': curr_list,
                   'y': percent_list}

        ####################
        # LABELS
        ####################
        goal_list = 'below $500', 'above $500 ~ below $1000', 'above $1000 ~ below $3000', 'above $3000 ~ below $5000', 'above $5000 ~ below $10000', 'above $10000 ~ below $50000', 'above $50000 ~ below $100000', 'above $100000'
        term_list = ['10 days or less', 'above 10 days and below 15 days', 'above 15 days and below 21 days', 'above 21 days and below 30 days', 'above 30 days and below 45 days', 'above 45 days and below 60 days', 'above 60 days']
        title_main = "Rate of success for '" + self.cate +"<br> when funding period is " + term_list[
            self.term_bin - 1] + "<br> and funding goal is " + goal_list[self.usd_goal_real_bin - 1]
        title = {'text': title_main}

        ####################
        # GRAPH
        ####################
        fig = go.Figure({"data": res_dct, "layout": {"title": title}})
        fig.update_traces(marker_color='#78BD40')

        fig.update_layout(title_x=0.5, xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Type of Currency")), yaxis=dict(tickformat="%"), font={'size': 9})

        html_str = plot(fig, output_type='div', include_plotlyjs=False)
        return html_str