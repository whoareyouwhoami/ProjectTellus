from django.shortcuts import render
from django.http import HttpResponse
from .forms import checkform

# View
def mainpage(request):
    if request.method == 'POST':
        form_x = checkform(request.POST)
    else:
        form_x = checkform()

    ref = {
        'form_x' : form_x
    }
    return render(request, 'kickstart/mainpage.html', ref)


