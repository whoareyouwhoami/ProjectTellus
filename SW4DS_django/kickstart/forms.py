from django import forms
from django.forms import ModelForm
from . import models
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime
# Year choice
year_choices = [x for x in range(2019,2031)]

class checkform(ModelForm):
    class Meta:
        model = models.DBform
        exclude = ['search_id', 'amount_usd','bin_term','bin_goal']
        labels = {
            'main_category':_('Main category'),
            'blurb':_('Description'),
            'location':_('Country'),
            'currency':_('Currency'),
            'goal':_('Amount')
        }
        widgets = {
            'date_start':forms.SelectDateWidget(years=year_choices),
            'date_end':forms.SelectDateWidget(years=year_choices)
        }
