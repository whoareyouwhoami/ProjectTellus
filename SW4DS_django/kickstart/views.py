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
    if request.method == 'POST':
        form_x = checkform(request.POST)
    else:
        form_x = checkform()

    ref = {
        'form_x' : form_x
    }
    return render(request, 'kickstart/mainpage.html', ref)


