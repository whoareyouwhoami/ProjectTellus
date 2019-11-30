from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import checkform
import requests
from django.contrib import messages

import required.keys as req

def to_main(request):
    response = redirect('/main/')
    return response
