from django import forms

## Main category choice
mcat_choices = [('', '---------'),('Art', 'Art'), ('Comics', 'Comics'), ('Crafts', 'Crafts'), ('Dance', 'Dance'),
               ('Design', 'Design'), ('Fashion', 'Fashion'), ('Film & Video', 'Film & Video'), ('Food', 'Food'),
               ('Games', 'Games'), ('Journalism', 'Journalism'), ('Music', 'Music'), ('Photography', 'Photography'),
               ('Publishing', 'Publishing'), ('Technology', 'Technology'), ('Theater', 'Theater')]
## Currency choice
currency_choices = [('0', '---------'), ('AUD', 'AUD'), ('CAD', 'CAD'), ('CHF', 'CHF'), ('DKK', 'DKK'), ('EUR', 'EUR'),
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

# Year choice
year_choices = [x for x in range(2019,2031)]

## Main Form
class checkform(forms.Form):
    main_category   = forms.ChoiceField(label='Main category', choices=mcat_choices)
    location        = forms.ChoiceField(label='Country', choices=country_choices)
    currency        = forms.ChoiceField(label='Currency', choices=currency_choices)
    date_start      = forms.DateField(widget=forms.SelectDateWidget(years=year_choices))
    date_end        = forms.DateField(widget=forms.SelectDateWidget(years=year_choices))
    goal            = forms.IntegerField(label='Amount')
