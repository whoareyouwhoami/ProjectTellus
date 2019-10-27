from django.shortcuts import render
from django.http import HttpResponse
from .forms import checkform

import required.data as data



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


