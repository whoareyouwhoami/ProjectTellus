"""
Kicktraq Web Crawling
"""

import os
import re
import time
import datetime
import pandas as pd
from datetime import datetime
from selenium import webdriver as wd
import SW4DS_django.database.db as dbt
from selenium.webdriver.chrome.options import Options

# Options
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

chrome_options = Options()
chrome_options.add_argument("--headless")

path = os.getcwd()

#########################
# Required Dictionaries
#########################
success_currency = {'AU$': 'AUD', 'CA$': 'CAD', 'HK$': 'HKD', 'MX$': 'MXN', 'NZ$': 'NZD', 'US$': 'USD', 'S$': 'SGD', 'SEK':'SEK','CHF':'CHF','NOK':'NOK','DKK':'DKK'}

curr_change = {'£':'GBP', '€':'EUR', 'CHF':'CHF', '¥':'JPY', 'SEK':'SEK','NOK':'NOK','DKK':'DKK'}

cur_loc = {'SEK': 'Sweden', 'NOK': 'Norway', 'DKK': 'Denmark', 'CHF': 'Switzerland', '£': 'UK', '¥': 'Japan', '€':'EU'}

country_list = ['AU','Australia', 'Canada', 'Denmark', 'Hong Kong', 'Japan', 'Mexico', 'New Zealand', 'Norway', 'UK', 'US', 'Sweden', 'Singapore', 'Switzerland']

us_states = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'}

country_cursym = {'AU': '$', 'Australia': '$', 'Canada': '$', 'Denmark': 'DKK', 'Hong Kong': '$', 'Japan': '¥', 'Mexico': '$', 'New Zealand': '$', 'Norway': 'NOK', 'UK': '£', 'US': '$', 'Sweden': 'SEK', 'Singapore': '$', 'Switzerland': 'CHF'}

country_cursign = {'AU': 'AUD', 'Australia': 'AUD', 'Canada': 'CAD', 'Denmark': 'DKK', 'Hong Kong': 'HKD', 'Japan': 'JPY', 'Mexico': 'MXN', 'New Zealand': 'NZD', 'Norway': 'NOK', 'UK': 'GBP', 'US': 'USD', 'Sweden': 'SEK', 'Singapore': 'SGD', 'Switzerland': 'CHF'}


month_str = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month_int = [1,2,3,4,5,6,7,8,9,10,11,12]
month_dict = dict(zip(month_str, month_int))


# 2019-11-29 currency rate
# currency_rate = {'AED': 3.67294, 'AFN': 78.488715, 'ALL': 111.366429, 'AMD': 477.643925, 'ANG': 1.718723, 'AOA': 490.921, 'ARS': 59.7836, 'AUD': 1.475547, 'AWG': 1.8, 'AZN': 1.7025, 'BAM': 1.776316, 'BBD': 2, 'BDT': 84.831426, 'BGN': 1.77644, 'BHD': 0.376993, 'BIF': 1874.266469, 'BMD': 1, 'BND': 1.364788, 'BOB': 6.909796, 'BRL': 4.1894, 'BSD': 1, 'BTC': 0.000131988977, 'BTN': 71.559511, 'BWP': 10.87353, 'BYN': 2.107897, 'BZD': 2.014168, 'CAD': 1.32892, 'CDF': 1663.774438, 'CHF': 0.999624, 'CLF': 0.024, 'CLP': 836.299391, 'CNH': 7.024966, 'CNY': 7.0194, 'COP': 3504.68892, 'CRC': 561.219026, 'CUC': 1, 'CUP': 25.75, 'CVE': 100.7, 'CZK': 23.218009, 'DJF': 178, 'DKK': 6.788803, 'DOP': 52.800507, 'DZD': 120.205945, 'EGP': 16.1166, 'ERN': 14.999703, 'ETB': 30.536398, 'EUR': 0.908684, 'FJD': 2.1911, 'FKP': 0.775819, 'GBP': 0.775819, 'GEL': 2.97, 'GGP': 0.775819, 'GHS': 5.573357, 'GIP': 0.775819, 'GMD': 51.15, 'GNF': 9527.068875, 'GTQ': 7.694292, 'GYD': 208.499132, 'HKD': 7.82628, 'HNL': 24.601971, 'HRK': 6.761144, 'HTG': 97.060976, 'HUF': 304.124977, 'IDR': 14114.6, 'ILS': 3.4737, 'IMP': 0.775819, 'INR': 71.785006, 'IQD': 1192.923651, 'IRR': 42105, 'ISK': 122.499995, 'JEP': 0.775819, 'JMD': 140.55937, 'JOD': 0.709, 'JPY': 109.562, 'KES': 102.89, 'KGS': 69.670113, 'KHR': 4074.453665, 'KMF': 447.849773, 'KPW': 900, 'KRW': 1179.24, 'KWD': 0.304129, 'KYD': 0.832751, 'KZT': 385.985803, 'LAK': 8858.904662, 'LBP': 1511.104191, 'LKR': 180.616256, 'LRD': 193.000002, 'LSL': 14.736115, 'LYD': 1.407021, 'MAD': 9.642889, 'MDL': 17.494842, 'MGA': 3680.764949, 'MKD': 55.907583, 'MMK': 1505.383821, 'MNT': 2688.612672, 'MOP': 8.056128, 'MRO': 357, 'MRU': 37.452432, 'MUR': 36.671983, 'MVR': 15.41, 'MWK': 735.774765, 'MXN': 19.441454, 'MYR': 4.1765, 'MZN': 64.06, 'NAD': 14.736115, 'NGN': 362.65, 'NIO': 33.70964, 'NOK': 9.190995, 'NPR': 114.495256, 'NZD': 1.554032, 'OMR': 0.38502, 'PAB': 1, 'PEN': 3.381954, 'PGK': 3.401662, 'PHP': 50.845, 'PKR': 155.140125, 'PLN': 3.930198, 'PYG': 6468.75888, 'QAR': 3.639072, 'RON': 4.3467, 'RSD': 106.86, 'RUB': 64.095, 'RWF': 932.664695, 'SAR': 3.750013, 'SBD': 8.267992, 'SCR': 13.699962, 'SDG': 45.079153, 'SEK': 9.54568, 'SGD': 1.366362, 'SHP': 0.775819, 'SLL': 7438.043346, 'SOS': 578.084428, 'SRD': 7.458, 'SSP': 130.26, 'STD': 21560.79, 'STN': 22.35, 'SVC': 8.74438, 'SYP': 515.029856, 'SZL': 14.736116, 'THB': 30.21, 'TJS': 9.687026, 'TMT': 3.51, 'TND': 2.8485, 'TOP': 2.3211, 'TRY': 5.744156, 'TTD': 6.751737, 'TWD': 30.508998, 'TZS': 2300.301993, 'UAH': 24.007175, 'UGX': 3697.282408, 'USD': 1, 'UYU': 37.91418, 'UZS': 9487.711828, 'VEF': 248487.642241, 'VES': 22704, 'VND': 23196.03724, 'VUV': 116.342107, 'WST': 2.643078, 'XAF': 596.057688, 'XAG': 0.05915423, 'XAU': 0.00068667, 'XCD': 2.70255, 'XDR': 0.728518, 'XOF': 596.057688, 'XPD': 0.00054318, 'XPF': 108.434855, 'XPT': 0.00111608, 'YER': 250.400036, 'ZAR': 14.627867, 'ZMW': 14.614141, 'ZWL': 322.000001}

currency_rate = dbt.currency_lst

chrome_options = Options()
chrome_options.add_argument("--headless")

class KicktraqOpen:
    def __init__(self, url):
        self.url = url
        self.driver = wd.Chrome(path + '/chromedriver', options=chrome_options)
        self.driver.get(self.url)

class WebcrawlClean(KicktraqOpen):
    def clean_amount(self, amount):
        # take out ,
        clamount = amount.replace(',', '')
        result = re.findall('\d+', clamount)[0]
        result = int(result)
        return result

    def conv_amount(self, amount, curr_t):
        # usd_pledged_real
        # usd_goal_real
        check_start = curr_t.split(' ')
        if len(check_start) == 2:
            curr_t = check_start[0]

        if curr_t != "USD" and curr_t != "USD (*)":
            curr_r = currency_rate[curr_t]
            new_amount = amount/curr_r
        else:
            new_amount = amount

        new_amount = round(new_amount,2)
        return new_amount

    def get_amount_bin(self, amountx):
        # usd_goal_real_bin
        goal_bin = (lambda x: '1' if x <= 500 else '2' if x <= 1000 else '3' if x <= 3000 else '4' if x <= 5000 else '5' if x <= 10000 else '6' if x <= 50000 else '7' if x <= 100000 else '8')(amountx)
        return goal_bin

    def conv_dt(self, datex):
        # converting date to YYYY-MM-DD format
        fmt = datex[-2:]
        convdtime = datetime.strptime(datex, '%Y %B %d' + fmt)
        convstime = convdtime.strftime("%Y-%m-%d")
        return convstime

    def get_term(self, start, end):
        startdate = datetime.strptime(start, "%Y-%m-%d").date()
        enddate = datetime.strptime(end, "%Y-%m-%d").date()
        diffdays = (enddate - startdate).days
        return diffdays

    def get_term_bin(self, term):
        term_bin = (lambda x: '1' if x <= 10 else '2' if x <= 15 else '3' if x <= 21 else '4' if x <= 30 else '5' if x <= 45 else '6' if x <= 60 else '7')(term)
        return term_bin


class KicktraqPage(WebcrawlClean):
    def __init__(self):
        super().__init__("https://www.kicktraq.com/projects/")

    def getdayone(self):
        self.dayonepage = "https://www.kicktraq.com/dayones/"
        return self.dayonepage

    def getarchive(self):
        self.archivepage = "https://www.kicktraq.com/archive/"
        return self.archivepage

    def get_curloc_type(self, currency_symb, detail_url):
        global currency_type
        global country_name

        self.currency_symb = currency_symb
        self.detail_url = detail_url

        self.driverx = wd.Chrome(path + '/chromedriver', options=chrome_options)
        self.driverx.get(self.detail_url)

        content = self.driverx.find_element_by_xpath("//div[@id='project-info-text']")
        content_lst = content.text.split('\n')

        funding_lst = [s for s in content_lst if "Funding:" in s]

        # TEMPORARY
        if len(funding_lst) == 0:
            funding_lst = [s for s in content_lst if "Funded:" in s]

        funding_goal = funding_lst[0].split(" of ")[1]

        # if the currency is in 'kr', get the country currency
        if currency_symb.isalpha():
            if currency_symb.lower() == 'k':
                currency_symb = funding_goal.split(" ")[1]  # get country for `kr` currency
            else:
                currency_symb = '$'


        ########################################
        # validate country for all currency
        ########################################
        content = self.driverx.find_element_by_id('button-backthis')
        prj_addr = content.get_attribute("href")
        self.new_driver = wd.Chrome(path + '/chromedriver', options=chrome_options)
        self.new_driver.get(prj_addr)

        ########################
        # KICKSTARTER page
        ########################

        # check if content exists
        # check_content > 0 : project DOES NOT exist
        # check_content = 0 : project exist
        check_content = self.new_driver.find_elements_by_xpath("//div[@id='hidden_project']")

        if len(check_content) != 0:
            # project DOES NOT exist
            if currency_symb == '$':
                currency_type = 'USD (*)'
                country_name = ''
            elif currency_symb in cur_loc:
                currency_type = currency_symb + ' (*)'
                country_name = ''
        else:
            # project exist

            # check if project is canceled
            # prj_status > 0 : project CANCELED
            # prj_status = 0 : project ongoing
            prj_status = self.new_driver.find_elements_by_xpath("//div[(@class='normal type-18')]")

            if len(prj_status) != 0:
                # project canceled

                # location
                loc = self.new_driver.find_elements_by_xpath("//div[@class='py2 py3-lg flex items-center auto-scroll-x']/a['nowrap navy-700 flex items-center medium mr3 type-12 keyboard-focusable']/span[@class='ml1']")
                locx = len(loc) - 1
                location = loc[locx].text
                region = location.split(',')[1].strip()

                if region == 'AU':
                    region = 'Australia'
                elif region in us_states:
                    region = 'US'

                if region in us_states:
                    region_cur = '$'
                elif region in country_cursym:
                    region_cur = country_cursym[region]
                else:
                    region_cur = '€'

                if currency_symb != region_cur:
                    # if 2nd page currency and 3rd page is different
                    if currency_symb == '$':  # assuming as USD as we do not know the country for $
                        currency_type = 'USD'
                    else:
                        currency_type = curr_change[currency_symb]
                else:
                    # if 2nd page currency and 3rd page is same
                    if region in country_list:
                        currency_type = country_cursign[region]
                    else:
                        currency_type = 'EUR'

                country_name = region

            else:
                # project is ongoing or successful

                # check if project is ongoing
                # check if project is ending soon
                prj_ongoing = self.new_driver.find_elements_by_xpath("//div[@class='ml5 ml0-lg']/div/div/span[@class='block type-16 type-28-md bold dark-grey-500']")
                prj_end_soon = self.new_driver.find_elements_by_xpath("//div[@class='ml5 ml0-lg']/div/div/span[@class='block type-16 type-28-md bold red-400']")

                # prj_ongoing  > 0 : project is running
                # prj_end_sonn > 0 : project is ending soon
                if len(prj_ongoing) != 0 or len(prj_end_soon) != 0:
                    # ongoing project
                    loc = self.new_driver.find_elements_by_xpath("//div[@class='py2 py3-lg flex items-center auto-scroll-x']/a['nowrap navy-700 flex items-center medium mr3 type-12 keyboard-focusable']/span[@class='ml1']")
                    locx = len(loc) - 1
                    location = loc[locx].text
                    region = location.split(',')[1].strip()

                    if region == 'AU':
                        region = 'Australia'
                    elif region in us_states:
                        region = 'US'

                    if region in us_states:
                        region_cur = '$'
                    elif region in country_cursym:
                        region_cur = country_cursym[region]
                    else:
                        region_cur = '€'

                    if currency_symb != region_cur:
                        # if 2nd page currency and 3rd page is different
                        if currency_symb == '$':  # assuming as USD as we do not know the country for $
                            currency_type = 'USD'
                        else:
                            currency_type = curr_change[currency_symb]
                    else:
                        # if 2nd page currency and 3rd page is same
                        if region in country_list:
                            currency_type = country_cursign[region]
                        else:
                            currency_type = 'EUR'

                    country_name = region
                else:
                    # project ended
                    get_money = self.new_driver.find_element_by_xpath("//div[@class='mb3']/h3[@class='mb0']/span[@class='money']").text
                    loc = self.new_driver.find_elements_by_xpath("//div[@class='NS_projects__category_location ratio-16-9 flex items-center']/a[@class='grey-dark mr3 nowrap type-12']")
                    location = loc[0].text
                    region = location.split(',')[1].strip()

                    if region == 'AU':
                        region = 'Australia'
                    elif region in us_states:
                        region = 'US'

                    # get the first currency sign of money
                    first_check = get_money[0]

                    if first_check != '$':
                        # will either be euro, pound, sek, nok, dkk, ....
                        if first_check not in ['£', '€', '¥']:
                            second_check = get_money.split(' ')
                            second_check_sign = second_check[0]
                            currency_type = success_currency[second_check_sign]
                        else:
                            currency_type = curr_change[first_check]

                    else:
                        currency_type = 'USD'

                    country_name = region

            self.new_driver.close()
        res_dict = {'currency_type': currency_type, 'country': country_name}
        self.driverx.close()
        return res_dict


    def getInfoSuccess(self, text, attrurl):
        backers = int(text.split("\n")[0].split(": ")[1])
        pledged = text.split('\n')[1].split(': ')[1].split(' of ')[0]
        goal = text.split('\n')[1].split(': ')[1].split(' of ')[1].split(' (')[0]
        year = text.split('\n')[3].split('(')[1][:-1]
        launched = text.split('\n')[3].split(": ")[1].split(' -> ')[0]
        deadline = text.split('\n')[3].split(": ")[1].split(' -> ')[1].split(' (')[0]

        month_start = month_dict.get(text.split('\n')[3].split(": ")[1].split(' -> ')[0].split(" ")[0])
        month_end = month_dict.get(text.split('\n')[3].split(": ")[1].split(' -> ')[1].split(' (')[0].split(" ")[0])

        if (month_end < month_start):
            start_year = str(int(year) - 1)
        else:
            start_year = year

        launched = start_year + ' ' + launched
        deadline = year + ' ' + deadline

        currency_t = goal[0]
        print("Currency at page 2:", currency_t)
        cur_loc_info = self.get_curloc_type(currency_t, attrurl)

        pledged = self.clean_amount(pledged)
        goal = self.clean_amount(goal)
        usd_pledged = self.conv_amount(pledged, cur_loc_info['currency_type'])
        usd_goal = self.conv_amount(goal, cur_loc_info['currency_type'])
        usd_goal_real_bin = self.get_amount_bin(usd_goal)
        launched = self.conv_dt(launched)
        deadline = self.conv_dt(deadline)

        term = self.get_term(launched, deadline)
        term_bin = self.get_term_bin(term)

        res_dct_pass = {'state': 'success',
                        'backers': backers,
                        'pledged': pledged,
                        'goal': goal,
                        'currency_type': cur_loc_info['currency_type'],
                        'country': cur_loc_info['country'],
                        'usd_pledged_real': usd_pledged,
                        'usd_goal_real': usd_goal,
                        'launched': launched,
                        'deadline': deadline,
                        'term': term,
                        'term_bin': term_bin,
                        'usd_goal_real_bin': usd_goal_real_bin
                        }

        return res_dct_pass

    def getInfoFail(self, text, attrurl):
        backers = int(text.split("\n")[0].split(": ")[1])
        pledged = text.split('\n')[1].split(': ')[1].split(' of ')[0]
        goal = text.split('\n')[1].split(': ')[1].split(' of ')[1].split(' (')[0]
        year = text.split('\n')[2].split('(')[1][:-1]
        launched = text.split('\n')[2].split(": ")[1].split(' -> ')[0]
        deadline = text.split('\n')[2].split(": ")[1].split(' -> ')[1].split(' (')[0]

        month_start = month_dict.get(text.split('\n')[2].split(": ")[1].split(' -> ')[0].split(" ")[0])
        month_end = month_dict.get(text.split('\n')[2].split(": ")[1].split(' -> ')[1].split(' (')[0].split(" ")[0])

        if (month_end < month_start):
            start_year = str(int(year) - 1)
        else:
            start_year = year

        launched = year + ' ' + launched
        deadline = year + ' ' + deadline

        currency_t = goal[0]
        print("Currency at page 2:", currency_t)
        cur_loc_info = self.get_curloc_type(currency_t, attrurl)

        pledged = self.clean_amount(pledged)
        goal = self.clean_amount(goal)
        usd_pledged = self.conv_amount(pledged, cur_loc_info['currency_type'])
        usd_goal = self.conv_amount(goal, cur_loc_info['currency_type'])
        usd_goal_real_bin = self.get_amount_bin(usd_goal)
        launched = self.conv_dt(launched)
        deadline = self.conv_dt(deadline)
        term = self.get_term(launched, deadline)
        term_bin = self.get_term_bin(term)

        res_dct_fail = {'state': 'fail',
                        'backers': backers,
                        'pledged': pledged,
                        'goal': goal,
                        'currency_type': cur_loc_info['currency_type'],
                        'country': cur_loc_info['country'],
                        'usd_pledged_real': usd_pledged,
                        'usd_goal_real': usd_goal,
                        'launched': launched,
                        'deadline': deadline,
                        'term': term,
                        'term_bin': term_bin,
                        'usd_goal_real_bin': usd_goal_real_bin
                        }

        return res_dct_fail


class KicktraqCrawl(KicktraqPage):
    def __init__(self):
        super().__init__()

    def webcrawl(self, start, end, text):
        print("Initiating crawling...")
        global collect

        self.timestart = time.time()
        self.start = start
        self.end = end
        self.text = text

        current_date = datetime.date(datetime.now())

        if self.text == "dayone":
            self.openpg = super().getdayone()
        elif self.text == "archive":
            self.openpg = super().getarchive()
        else:
            return "Either `dayone` or `archive` page available"

        for page in range(self.start, self.end + 1):
            print("==================================")
            print("Collecting page", page, "of",self.text,"......")
            print("==================================")

            self.driver.get('{}?page={}'.format(self.openpg, page))

            # Common
            prj_list = self.driver.find_elements_by_xpath("//div[@class='project-infobox']")
            prj_length = len(prj_list)

            for i in range(prj_length):
                print(">> Collecting project",i,"right now...")
                x = prj_list[i]
                p1 = x.find_element_by_xpath("h2/a")
                detail_url = p1.get_attribute("href")

                # Project Title
                name = p1.text
                name = name.replace("'", "")

                # Project Content
                blurb = x.find_element_by_xpath("div[not(@class)]").text
                blurb = blurb.replace("'", "")

                # if `blurb` is not empty
                if blurb != "":

                    # Project Category
                    cat = x.find_element_by_xpath("div[@class='project-cat']")
                    cat_lst = cat.find_elements_by_tag_name("a")
                    category = cat_lst[0].text

                    # Project Information
                    info = x.find_element_by_xpath("div[@class='project-infobits']/div[@class='project-details']")
                    prj_info = info.text

                    # funding rate
                    rate_info = info.find_element_by_tag_name("span").text
                    percent = int(re.findall('\d+', rate_info)[0])

                    if percent >= 100 and self.text == 'dayone':
                        collect = super().getInfoSuccess(prj_info, detail_url)
                    elif percent < 100 and self.text == 'archive':
                        collect = super().getInfoFail(prj_info, detail_url)
                    else:
                        collect = {}

                    if len(collect) != 0:
                        main_dct = {'collected_date': current_date,
                                    'updated_date': current_date,
                                    'name': name,
                                    'blurb': blurb,
                                    'category': category,
                                    'funding_rate': percent}

                        if collect['country'] != '':
                            # merging results
                            main_dct.update(collect)
                            # print(main_dct)
                            print('Country:', main_dct['country'])
                            print('Currency type:', main_dct['currency_type'])

                            row_sql = dbt.DBcls.sqlselect(main_dct)
                            dbt.cur.execute(row_sql)
                            chk_row = dbt.cur.rowcount
                            get_row = dbt.cur.fetchone()
                            # print(chk_row)
                            if chk_row == 0:
                                insert_sql = dbt.DBcls.sqlinsert()
                                print("Query:", insert_sql)
                                dbt.cur.execute(insert_sql, main_dct)
                                print("Inserted in database\n")

                            else:
                                print("Data already exist. Updating to new information...")
                                get_id = get_row['id']
                                update_sql = dbt.DBcls.sqlupdate(get_id, main_dct)
                                print("Query:", update_sql, '\n')
                                dbt.cur.execute(update_sql)
                        else:
                            pass


        print("==================================")
        print("!COMPLETED!")
        print("==================================")
        print("Completed in {} seconds...".format(round(time.time() - self.timestart),2))

    def quitWeb(self):
        qt = self.driver.close()
        return qt


# Example
a = KicktraqCrawl()
a.webcrawl(1,10,"dayone")
a.webcrawl(20,25,"archive")
# ...
# ...
a.quitWeb()
# dbt.DBcls.clcn()