from django.db import models
from django.utils.timezone import now

## Main category choice
mcat_choices = [('', '---------'),('Art', 'Art'), ('Comics', 'Comics'), ('Crafts', 'Crafts'), ('Dance', 'Dance'),
               ('Design', 'Design'), ('Fashion', 'Fashion'), ('Film & Video', 'Film & Video'), ('Food', 'Food'),
               ('Games', 'Games'), ('Journalism', 'Journalism'), ('Music', 'Music'), ('Photography', 'Photography'),
               ('Publishing', 'Publishing'), ('Technology', 'Technology'), ('Theater', 'Theater')]
## Currency choice
currency_choices = [('', '---------'), ('AUD', 'AUD'), ('CAD', 'CAD'), ('EUR', 'EUR'),
                    ('GBP', 'GBP'), ('SGD', 'SGD'), ('USD', 'USD')]

## Country choice
country_choices = [('', '---------'), ('Australia', 'Australia'),('Canada', 'Canada'), ('France', 'France'),
                   ('Germany', 'Germany'), ('Italy', 'Italy'), ('Singapore', 'Singapore'), ('Spain', 'Spain'),
                   ('Neterlands', 'the Neterlands'), ('UK', 'the United Kingdom'), ('US', 'the United States')]


from datetime import datetime
class DBform(models.Model):
    search_id = models.AutoField(primary_key=True)
    main_category = models.CharField(max_length=100, choices=mcat_choices)
    blurb = models.TextField()
    location = models.CharField(max_length=100, choices=country_choices)
    currency = models.CharField(max_length=100, choices=currency_choices)
    date_start = models.DateField(default=now)
    date_end = models.DateField(default=now)
    goal = models.PositiveIntegerField()
    amount_usd = models.FloatField()
    bin_term = models.PositiveIntegerField()
    bin_goal = models.PositiveIntegerField()

