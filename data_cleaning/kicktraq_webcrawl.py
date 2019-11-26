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

pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

path = os.getcwd()

# DataFrame for result
blurb_df = pd.DataFrame(columns = ['collected_date','name', 'blurb', 'state', 'category',
                                   'funding_rate', 'pledged', 'goal','currency_type', 'usd_pledged_real', 'usd_goal_real',
                                   'launched', 'deadline', 'term','term_bin', 'usd_goal_real_bin'])

success_currency = {'AU$': 'AUD', 'CA$': 'CAD', 'HK$': 'HKD', 'MX$': 'MXN', 'NZ$': 'NZD', 'US$': 'USD', 'S$': 'SGD'}

unsuccess_currency = {'AU':'AUD', 'Australia': 'AUD', 'Canada': 'CAD', 'Hong Kong': 'HKD', 'Mexico': 'MXN', 'NZ': 'NZD', 'Singapore': 'SGD'}

currfix = ['£','€','CHF','¥']

curr_change = {'£':'GBP', '€':'EUR', 'CHF':'CHF', '¥':'JPY'}

# 2019-11-26 currency rate
currency_rate = {'AED': 3.6732, 'AFN': 78.813395, 'ALL': 111.387139, 'AMD': 477.766294, 'ANG': 1.71589, 'AOA': 475.1455, 'ARS': 59.656064, 'AUD': 1.474668, 'AWG': 1.8, 'AZN': 1.7025, 'BAM': 1.77655, 'BBD': 2, 'BDT': 84.841984, 'BGN': 1.7763, 'BHD': 0.377006, 'BIF': 1876.459218, 'BMD': 1, 'BND': 1.365996, 'BOB': 6.91879, 'BRL': 4.2272, 'BSD': 1, 'BTC': 0.000138221454, 'BTN': 71.753547, 'BWP': 10.875574, 'BYN': 2.065464, 'BZD': 2.016777, 'CAD': 1.331, 'CDF': 1665.879771, 'CHF': 0.99641, 'CLF': 0.024, 'CLP': 828.799556, 'CNH': 7.026137, 'CNY': 7.0313, 'COP': 3426.198207, 'CRC': 572.689305, 'CUC': 1, 'CUP': 25.75, 'CVE': 100.375, 'CZK': 23.1504, 'DJF': 178, 'DKK': 6.784255, 'DOP': 52.833199, 'DZD': 120.168016, 'EGP': 16.1341, 'ERN': 14.999746, 'ETB': 30.230392, 'EUR': 0.907964, 'FJD': 2.1916, 'FKP': 0.775434, 'GBP': 0.775434, 'GEL': 2.975, 'GGP': 0.775434, 'GHS': 5.573092, 'GIP': 0.775434, 'GMD': 51.1, 'GNF': 9535.428748, 'GTQ': 7.701775, 'GYD': 208.708126, 'HKD': 7.82689, 'HNL': 24.633271, 'HRK': 6.752405, 'HTG': 97.302351, 'HUF': 305.07, 'IDR': 14086.1, 'ILS': 3.46555, 'IMP': 0.775434, 'INR': 71.672507, 'IQD': 1194.465451, 'IRR': 42105, 'ISK': 122.939982, 'JEP': 0.775434, 'JMD': 140.55937, 'JOD': 0.709, 'JPY': 108.982, 'KES': 102.1, 'KGS': 69.670021, 'KHR': 4060.068987, 'KMF': 447.349843, 'KPW': 900, 'KRW': 1175.51, 'KWD': 0.303695, 'KYD': 0.833757, 'KZT': 386.385911, 'LAK': 8865.709957, 'LBP': 1513.018384, 'LKR': 181.049492, 'LRD': 193.049961, 'LSL': 14.727118, 'LYD': 1.408076, 'MAD': 9.659874, 'MDL': 17.40961, 'MGA': 3678.461869, 'MKD': 55.885332, 'MMK': 1515.808652, 'MNT': 2688.420135, 'MOP': 8.066072, 'MRO': 357, 'MRU': 37.499262, 'MUR': 36.602138, 'MVR': 15.4, 'MWK': 737.434911, 'MXN': 19.4476, 'MYR': 4.1805, 'MZN': 64.011999, 'NAD': 14.727319, 'NGN': 362.7, 'NIO': 33.752513, 'NOK': 9.1757, 'NPR': 114.791337, 'NZD': 1.557297, 'OMR': 0.384985, 'PAB': 1, 'PEN': 3.390362, 'PGK': 3.405952, 'PHP': 50.792825, 'PKR': 156.283679, 'PLN': 3.902061, 'PYG': 6468.632579, 'QAR': 3.643061, 'RON': 4.3331, 'RSD': 106.775, 'RUB': 63.9287, 'RWF': 933.614923, 'SAR': 3.750187, 'SBD': 8.267992, 'SCR': 13.699476, 'SDG': 45.136225, 'SEK': 9.63424, 'SGD': 1.36523, 'SHP': 0.775434, 'SLL': 7438.043346, 'SOS': 578.775762, 'SRD': 7.458, 'SSP': 130.26, 'STD': 21560.79, 'STN': 22.4, 'SVC': 8.754496, 'SYP': 514.995156, 'SZL': 14.722213, 'THB': 30.235, 'TJS': 9.692844, 'TMT': 3.5, 'TND': 2.846, 'TOP': 2.320065, 'TRY': 5.74277, 'TTD': 6.760437, 'TWD': 30.505052, 'TZS': 2302.207123, 'UAH': 24.057369, 'UGX': 3702.021093, 'USD': 1, 'UYU': 37.785223, 'UZS': 9515.331052, 'VEF': 248487.642241, 'VES': 22704, 'VND': 23201.13598, 'VUV': 116.36648, 'WST': 2.641719, 'XAF': 595.585478, 'XAG': 0.05927682, 'XAU': 0.00068749, 'XCD': 2.70255, 'XDR': 0.728233, 'XOF': 595.585478, 'XPD': 0.00055444, 'XPF': 108.348951, 'XPT': 0.0011136, 'YER': 250.349961, 'ZAR': 14.76184, 'ZMW': 14.437728, 'ZWL': 322.000001}


class KicktraqOpen:
    def __init__(self, url):
        self.url = url
        self.driver = wd.Chrome(path + '/chromedriver')
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
        if curr_t != "USD":
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

    def get_currency_type(self, currency_symb, detail_url):
        global currency_type

        self.currency_symb = currency_symb
        self.detail_url = detail_url

        self.driverx = wd.Chrome(path + '/chromedriver')
        self.driverx.get(self.detail_url)

        content = self.driverx.find_element_by_xpath("//div[@id='project-info-text']")
        content_lst = content.text.split('\n')

        funding_lst = [s for s in content_lst if "Funding:" in s]

        # TEMPORARY
        if len(funding_lst) == 0:
            funding_lst = [s for s in content_lst if "Funded:" in s]

        funding_goal = funding_lst[0].split(" of ")[1]

        if self.currency_symb == 'k':
            currency_type = funding_goal.split(" ")[1]  # get country for `kr` currency


        else:  # for `$`
            content = self.driverx.find_element_by_id('button-backthis')
            prj_addr = content.get_attribute("href")
            self.new_driver = wd.Chrome(path + '/chromedriver')
            self.new_driver.get(prj_addr)

            # check if project is successful or not
            check_content = self.new_driver.find_elements_by_xpath("//div[@id='hidden_project']")
            if len(check_content) != 0:
                currency_type = "USD (*)"
            else:
                prj_status = self.new_driver.find_elements_by_xpath("//div[(@class='normal type-18')]")
                if len(prj_status) != 0:
                    # if project is unsuccessful
                    # get location
                    loc = self.new_driver.find_elements_by_xpath("//div[@class='py2 py3-lg flex items-center auto-scroll-x']/a['nowrap navy-700 flex items-center medium mr3 type-12 keyboard-focusable']/span[@class='ml1']")
                    locx = int((len(loc) / 2) - 1)
                    location = loc[locx].text
                    region = location.split(",")[1].strip()

                    # get currency
                    if region in unsuccess_currency:
                        currency_type = unsuccess_currency[region]
                    else:
                        currency_type = "USD"
                else:
                    # if project is successful
                    # check if project is ongoing
                    prj_ongoing = self.new_driver.find_elements_by_xpath("//div[@class='ml5 ml0-lg']/div/div/span[@class='block type-16 type-28-md bold dark-grey-500']")
                    prj_end_soon = self.new_driver.find_elements_by_xpath("//div[@class='ml5 ml0-lg']/div/div/span[@class='block type-16 type-28-md bold red-400']")

                    if len(prj_ongoing) != 0 or len(prj_end_soon) != 0:
                        # if project is ongoing
                        loc = self.new_driver.find_elements_by_xpath("//div[@class='py2 py3-lg flex items-center auto-scroll-x']/a['nowrap navy-700 flex items-center medium mr3 type-12 keyboard-focusable']/span[@class='ml1']")
                        locx = int((len(loc) / 2) - 1)
                        location = loc[locx].text
                        region = location.split(",")[1].strip()

                        # get currency
                        if region in unsuccess_currency:
                            currency_type = unsuccess_currency[region]
                        else:
                            currency_type = "USD"

                    else:
                        # if project ended
                        # if project is successful
                        get_money = self.new_driver.find_element_by_xpath("//div[@class='mb3']/h3[@class='mb0']/span[@class='money']").text
                        first_check = get_money[0]

                        if first_check != '$':
                            get_money_sp = get_money.split(" ")
                            check_curr_note = get_money_sp[0]
                        else:
                            check_curr_note = first_check

                        if check_curr_note in success_currency:
                            currency_type = success_currency[check_curr_note]
                        else:
                            currency_type = "USD"

            self.new_driver.close()
        self.driverx.close()
        return currency_type

    def getInfoSuccess(self, text, attrurl):
        backers = int(text.split("\n")[0].split(": ")[1])
        pledged = text.split('\n')[1].split(': ')[1].split(' of ')[0]
        goal = text.split('\n')[1].split(': ')[1].split(' of ')[1].split(' (')[0]
        year = text.split('\n')[3].split('(')[1][:-1]
        launched = text.split('\n')[3].split(": ")[1].split(' -> ')[0]
        deadline = text.split('\n')[3].split(": ")[1].split(' -> ')[1].split(' (')[0]

        launched = year + ' ' + launched
        deadline = year + ' ' + deadline

        currency_t = goal[0]

        if currency_t not in currfix:
            currency_t = self.get_currency_type(currency_t, attrurl)
        else:
            currency_t = curr_change[currency_t]

        pledged = self.clean_amount(pledged)
        goal = self.clean_amount(goal)
        usd_pledged = self.conv_amount(pledged, currency_t)
        usd_goal = self.conv_amount(goal, currency_t)
        usd_goal_real_bin = self.get_amount_bin(usd_goal)
        launched = self.conv_dt(launched)
        deadline = self.conv_dt(deadline)

        term = self.get_term(launched, deadline)
        term_bin = self.get_term_bin(term)

        res_dct_pass = {'state': ['success'],
                        'backers': [backers],
                        'pledged': [pledged],
                        'goal': [goal],
                        'currency_type': [currency_t],
                        'usd_pledged_real': [usd_pledged],
                        'usd_goal_real': [usd_goal],
                        'launched': [launched],
                        'deadline': [deadline],
                        'term': [term],
                        'term_bin': [term_bin],
                        'usd_goal_real_bin': [usd_goal_real_bin]
                        }

        return res_dct_pass

    def getInfoFail(self, text, attrurl):
        backers = int(text.split("\n")[0].split(": ")[1])
        pledged = text.split('\n')[1].split(': ')[1].split(' of ')[0]
        goal = text.split('\n')[1].split(': ')[1].split(' of ')[1].split(' (')[0]
        year = text.split('\n')[2].split('(')[1][:-1]
        launched = text.split('\n')[2].split(": ")[1].split(' -> ')[0]
        deadline = text.split('\n')[2].split(": ")[1].split(' -> ')[1].split(' (')[0]

        launched = year + ' ' + launched
        deadline = year + ' ' + deadline

        currency_t = goal[0]

        if currency_t not in currfix:
            currency_t = self.get_currency_type(currency_t, attrurl)
        else:
            currency_t = curr_change[currency_t]

        pledged = self.clean_amount(pledged)
        goal = self.clean_amount(goal)
        usd_pledged = self.conv_amount(pledged, currency_t)
        usd_goal = self.conv_amount(goal, currency_t)
        usd_goal_real_bin = self.get_amount_bin(usd_goal)
        launched = self.conv_dt(launched)
        deadline = self.conv_dt(deadline)
        term = self.get_term(launched, deadline)
        term_bin = self.get_term_bin(term)

        res_dct_fail = {'state': ['fail'],
                        'backers': [backers],
                        'pledged': [pledged],
                        'goal': [goal],
                        'currency_type': [currency_t],
                        'usd_pledged_real': [usd_pledged],
                        'usd_goal_real': [usd_goal],
                        'launched': [launched],
                        'deadline': [deadline],
                        'term': [term],
                        'term_bin': [term_bin],
                        'usd_goal_real_bin': [usd_goal_real_bin]
                        }

        return res_dct_fail


class KicktraqCrawl(KicktraqPage):
    def __init__(self):
        super().__init__()

    def webcrawl(self, start, end, text):
        global collect
        global blurb_df

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
            print("Collecting page", page, "......")
            print("==================================")

            self.driver.get('{}?page={}'.format(self.openpg, page))

            # Common
            prj_list = self.driver.find_elements_by_xpath("//div[@class='project-infobox']")
            prj_length = len(prj_list)

            for i in range(prj_length):
                print(">> Collecting prioject",i,"right now...")
                x = prj_list[i]
                p1 = x.find_element_by_xpath("h2/a")
                detail_url = p1.get_attribute("href")

                # Project Title
                name = p1.text

                # Project Content
                blurb = x.find_element_by_xpath("div[not(@class)]").text

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
                        main_dct = {'collected_date': [current_date],
                                    'name': [name],
                                    'blurb': [blurb],
                                    'category': [category],
                                    'funding_rate': [percent]}


                        # merging results
                        main_dct.update(collect)
                        print(main_dct)
                        dfx = pd.DataFrame(main_dct)
                        blurb_df = blurb_df.append(dfx, sort=False, ignore_index=True)


        print("==================================")
        print("!COMPLETED!")
        print("==================================")
        print("Completed in {} seconds...".format(round(time.time() - self.timestart),2))

    def quitWeb(self):
        qt = self.driver.close()
        return qt


# Example
# a = KicktraqCrawl()
# a.webcrawl(1,2,"dayone")
# ...
# ...
# a.quitWeb()