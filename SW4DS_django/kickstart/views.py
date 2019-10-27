from django.shortcuts import render
from django.http import HttpResponse
from .forms import checkform
import requests


import required.data as data
import required.keys as req



## Ajax for category list
cat = data.data_fin.groupby(('main_category','category')).count().reset_index()
cat_group = cat[['main_category','category']]

def load_cat(request):
    """
    Getting list of categories that corresponds to main category and sends them to category_list.html to create <option> tags.
    Category list will then be updated by AJAX.
    """

    # get main category
    mcat_id = request.GET.get('main_category')

    # checks if main category exist in data
    # else return empty list
    current_mcat = cat_group.loc[cat_group['main_category'] == mcat_id]
    if len(current_mcat) > 0:
        cat_lst = current_mcat['category'].to_list()
    else:
        cat_lst = []

    return render(request, 'kickstart/category_list.html', {'categories':cat_lst})

## Data cleaning
def get_currency(curr, amount):
    """
     This function converts currency into USD
     Curerncy rate is taken from https://openexchangerates.org using api
    """

    # get api response
    response = requests.get('https://openexchangerates.org/api/latest.json?app_id=' + req.api_key)
    currency_data = response.json()
    currency_lst = currency_data['rates']

    curr = curr.upper()

    # converts all currency based on USD
    if curr != "USD":
        currency_rate = currency_lst[curr]
        new_amount = currency_rate * amount
    else:
        new_amount = amount

    return new_amount

def get_term_bin(start,end):
    """
    Binning project period
    Result will return a value from 1 to 7
    """
    # project period in days
    date_diff = end - start
    day_diff = date_diff.days

    # binning function
    term_bin_fnc = lambda x: '1' if x <= 10 else '2' if x <= 15 else '3' if x <= 21 else '4' if x <= 30 else '5' if x <= 45 else '6' if x <= 60 else '7'

    binning = term_bin_fnc(day_diff)

    return binning

## View
def mainpage(request):
    global ref

    if request.method == 'POST':
        form_x = checkform(request.POST)

        # get category value separately
        cat = request.POST.get('category')

        if form_x.is_valid():
            main_category = form_x.cleaned_data['main_category']
            location = form_x.cleaned_data['location']
            currency = form_x.cleaned_data['currency']
            date_start = form_x.cleaned_data['date_start']
            date_end = form_x.cleaned_data['date_end']
            goal = form_x.cleaned_data['goal']

            # cleaning category value
            mcat_lst = cat_group.loc[cat_group['main_category'] == main_category]
            cat_lst = mcat_lst['category'].to_list()

            if cat not in cat_lst:
                # testing code 1
                print("Wrong category value")
                category = ""
                msg = "Something went wrong"
            else:
                category = cat
                msg = "Successful"

            cat_lst_length = len(cat_lst)

            # list of details to send it to html page
            ref = {
                'form_x': form_x,
                'cat_lst': cat_lst,
                'cat': category,
                'cat_lst_length': cat_lst_length,
                'msg': msg,
            }
            # testing code 2
            print(main_category, category, location, currency, date_start, date_end, goal)
    else:
        form_x = checkform()
        ref = {
            'form_x': form_x,
        }

    return render(request, 'kickstart/mainpage.html', ref)


