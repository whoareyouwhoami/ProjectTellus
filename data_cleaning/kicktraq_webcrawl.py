#!/usr/bin/env python3

"""
Kicktraq Web Crawling
"""
import sys
import os
import re
import time
import datetime
import pandas as pd
from datetime import datetime
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options

# Options
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

chrome_options = Options()
chrome_options.add_argument("--headless")

############
# LOCAL
############
import SW4DS_django.database.db as dbt
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


currency_rate = dbt.currency_lst
print("Currency rate called")

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

        print("opening 2nd driver")
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
        print("opening 3rd driver")
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
        print("opening 1st driver")
        super().__init__()
        print("1st driver opened")

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

# ...
# ...
a.quitWeb()
# dbt.DBcls.clcn()