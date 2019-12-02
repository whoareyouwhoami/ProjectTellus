from django.db import models

## Main category choice
mcat_choices = [('', '---------'),('Art', 'Art'), ('Comics', 'Comics'), ('Crafts', 'Crafts'), ('Dance', 'Dance'),
               ('Design', 'Design'), ('Fashion', 'Fashion'), ('Film & Video', 'Film & Video'), ('Food', 'Food'),
               ('Games', 'Games'), ('Journalism', 'Journalism'), ('Music', 'Music'), ('Photography', 'Photography'),
               ('Publishing', 'Publishing'), ('Technology', 'Technology'), ('Theater', 'Theater')]
## Currency choice
currency_choices = [('', '---------'), ('AUD', 'AUD'), ('CAD', 'CAD'), ('CHF', 'CHF'), ('DKK', 'DKK'), ('EUR', 'EUR'),
                   ('GBP', 'GBP'), ('HKD', 'HKD'), ('JPY', 'JPY'), ('MXN', 'MXN'), ('NOK', 'NOK'), ('NZD', 'NZD'),
                   ('SEK', 'SEK'), ('SGD', 'SGD'), ('USD', 'USD')]

## Country choice
country_choices = [('', '---------'), ('Australia', 'Australia'), ('Austria', 'Austria'), ('Belgium', 'Belgium'),
                   ('Canada', 'Canada'), ('Denmark', 'Denmark'), ('France', 'France'), ('Germany', 'Germany'),
                   ('Hong Kong', 'Hong Kong'), ('Ireland', 'Ireland'), ('Italy', 'Italy'), ('Japan', 'Japan'),
                   ('Luxembourg', 'Luxembourg'), ('Mexico', 'Mexico'), ('New Zealand', 'New Zealand'),
                   ('Norway', 'Norway'), ('Singapore', 'Singapore'), ('Spain', 'Spain'), ('Sweden', 'Sweden'),
                   ('Switzerland', 'Switzerland'), ('the Neterlands', 'the Neterlands'),
                   ('the United Kingdom', 'the United Kingdom'), ('the United States', 'the United States')]

import datetime
from datetime import datetime
class DBform(models.Model):
    search_id = models.AutoField(primary_key=True)
    main_category = models.CharField(max_length=100, choices=mcat_choices)
    blurb = models.TextField()
    location = models.CharField(max_length=100, choices=country_choices)
    currency = models.CharField(max_length=100, choices=currency_choices)
    date_start = models.DateField(default=datetime.today())
    date_end = models.DateField(default=datetime.today())
    goal = models.PositiveIntegerField()
    amount_usd = models.FloatField()
    bin_term = models.PositiveIntegerField()
    bin_goal = models.PositiveIntegerField()

