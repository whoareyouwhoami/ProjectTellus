from django.shortcuts import render
from django.http import HttpResponse
from .forms import checkform

import required.data as data

## Ajax
cat = data.data_fin.groupby(('main_category','category')).count().reset_index()
cat_group = cat[['main_category','category']]

def load_cat(request):
    mcat_id = request.GET.get('main_category')
    current_mcat = cat_group.loc[cat_group['main_category'] == mcat_id]
    cat_lst = current_mcat['category'].to_list()
    return render(request, 'kickstart/category_list.html',{'categories':cat_lst})



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


