import sys
import requests
import pandas as pd
from .forms import checkform
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date

import visual.viscls as vis
import MLcall.mlres as mlc
import database.currency_call as cc

change_country = {'Neterlands' : 'the Neterlands', 'UK' : 'the United Kingdom', 'US' : 'the United States'}

class FormClean:
    def __init__(self):
        self.text = 'testing'

    def get_currency(self, curr, amount):
        # converts currency rate to USD
        self.curr = curr.upper()
        self.amount = amount

        if self.curr != 'USD':
            currency_lst = cc.currency_lst
            currency_rate = currency_lst[self.curr]
            new_amount = round((self.amount/currency_rate),2)
        else:
            new_amount = self.amount

        return new_amount

    def get_term_bin(self, start, end):
        # binning project term period
        self.start = start
        self.end = end

        dt_diff = (self.end - self.start).days
        term_bin_fnc = lambda x: '1' if x <= 10 else '2' if x <= 15 else '3' if x <= 21 else '4' if x <= 30 else '5' if x <= 45 else '6' if x <= 60 else '7'
        binning = term_bin_fnc(dt_diff)

        return binning

    def get_goal_bin(self, amount):
        self.amount = amount

        goal_bin_fnc = lambda \
            x: '1' if x <= 500 else '2' if x <= 1000 else '3' if x <= 3000 else '4' if x <= 5000 else '5' if x <= 10000 else '6' if x <= 50000 else '7' if x <= 100000 else '8'
        binning = goal_bin_fnc(self.amount)

        return binning

    #####################
    # TEMPORARY
    #####################
    def get_daydiff(self, start, end):
        self.start = start
        self.end = end
        dt_diff = (self.end - self.start).days
        return dt_diff

########################
# VIEW
########################
def mainpage(request):
    if request.method == 'POST':
        form_x = checkform(request.POST)
        x = FormClean()

        if form_x.is_valid():
            print("Searched at", datetime.now())

            main_category = form_x.cleaned_data['main_category']
            blurb = form_x.cleaned_data['blurb']
            location = form_x.cleaned_data['location']
            currency = form_x.cleaned_data['currency']
            date_start = form_x.cleaned_data['date_start']
            date_end = form_x.cleaned_data['date_end']
            goal = form_x.cleaned_data['goal']

            today_date = date.today()
            day_diff = x.get_daydiff(date_start, date_end)


            if date_start < today_date or date_end < today_date:
                messages.error(request, "Please enter proper duration.")
                return render(request, 'kickstart/mainpage.html', {'form_x': form_x})
            elif day_diff < 0:
                messages.error(request, "Please enter proper duration.")
                return render(request, 'kickstart/mainpage.html', {'form_x': form_x})
            else:
                messages.success(request, 'See your result below...')
                amount_usd = x.get_currency(currency, goal)
                bin_term = x.get_term_bin(date_start, date_end)
                bin_goal = x.get_goal_bin(amount_usd)

                xtra = form_x.save(commit=False)
                xtra.amount_usd = amount_usd
                xtra.bin_term = bin_term
                xtra.bin_goal = bin_goal
                xtra.save()

                bin_term = int(bin_term)
                bin_goal = int(bin_goal)

                visx = vis.VisCls(main_category, bin_term, bin_goal)

                ##################
                # GRAPH
                ##################
                html_success_term = visx.g_success_term()
                html_goal_dist = visx.g_goal_dist()
                html_pledge_pp = visx.g_pledge_pp()
                html_succes_cat_amount = visx.g_success_cat_amount()
                html_success_curr = visx.g_success_by_curr()

                ##################
                # ML
                ##################
                mldct = {'main_category': main_category,
                         'blurb':blurb,
                         'country':location,
                         'currency':currency,
                         'usd_goal_real' : bin_goal,
                         'launched_year':date_start.year,
                         'launched_month': date_start.month,
                         'launched_day': date_start.day,
                         'term': day_diff,
                         }

                mlpd = pd.DataFrame([mldct])
                mlval = mlc.the_function(mlpd)

                if location in change_country:
                    country = change_country[location]
                else:
                    country = location

                ##################
                # RESULT
                ##################
                context = {'main_category': main_category,
                           'blurb':blurb,
                           'country': country,
                           'currency': currency,
                           'date_start': date_start,
                           'date_end': date_end,
                           'project_period' : day_diff,
                           'goal': goal,
                           'goal_usd': amount_usd,
                           'form_x': form_x,
                           'html_success_term': html_success_term,
                           'html_goal_dist': html_goal_dist,
                           'html_pledge_pp': html_pledge_pp,
                           'html_succes_cat_amount': html_succes_cat_amount,
                           'html_success_curr': html_success_curr,
                           'mlval':mlval,
                           }

                return render(request, 'kickstart/mainpage.html', context)
        else:
            form_x = checkform()
            messages.error(request, "Something is not right... Check your inputs!")
    else:
        form_x = checkform()

    ref = {'form_x': form_x}
    return render(request, 'kickstart/mainpage.html', ref)

