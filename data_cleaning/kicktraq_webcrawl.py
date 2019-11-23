"""
- 프로젝트 대부분이 정시에 끝나서 crontab 사용시 40분에 시작하여 최대 20분안에 끝나게 만든다.
"""

import os
import re
import time
import pandas as pd
import numpy as np
import requests
from datetime import datetime
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys

pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

path = os.getcwd()
# driver = wd.Chrome(path + '/chromedriver')

# DataFrame for result
blurb_df = pd.DataFrame(columns = ['collected_date','name', 'blurb', 'state', 'category',
                                   'funding_rate', 'pledged', 'goal','currency_type',
                                   'launched', 'deadline'])


success_currency = {'AU$': 'AUD', 'CA$': 'CAD', 'HK$': 'HKD', 'MX$': 'MXN', 'NZ$': 'NZD', 'US$': 'USD', 'S$': 'SGD'}

unsuccess_currency = {'AU':'AUD', 'Australia': 'AUD', 'Canada': 'CAD', 'Hong Kong': 'HKD', 'Mexico': 'MXN', 'NZ': 'NZD', 'Singapore': 'SGD'}

currfix = ['£','€','CHF','¥']



class KicktraqOpen:
    def __init__(self, url):
        self.url = url
        self.driver = wd.Chrome(path + '/chromedriver')
        self.driver.get(self.url)

class KicktraqPage(KicktraqOpen):
    def __init__(self):
        super().__init__("https://www.kicktraq.com/projects/")

    def getdayone(self):
        self.dayonepage = "https://www.kicktraq.com/dayones/"
        # self.driver.get(self.dayonepage)
        return self.dayonepage

    def getarchive(self):
        self.archivepage = "https://www.kicktraq.com/archive/"
        # self.driver.get(self.archivepage)
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

            ## check if project is successful or not
            check_content = self.new_driver.find_elements_by_xpath("//div[@id='hidden_project']")
            if len(check_content) != 0:
                currency_type = "USD (*)"
            else:
                prj_status = self.new_driver.find_elements_by_xpath("//div[(@class='normal type-18')]")
                if len(prj_status) != 0:
                    ## if project is unsuccessful
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

                    # get money
                    # goal_val = new_driver.find_elements_by_xpath(
                    #     "//div[@class='flex items-center']/span['ksr-green-700 inline-block bold type-16 type-28-md']/span['soft-black']")[
                    #     1].text.split(" ")[1].replace(',', '')
                    # pledge_val = new_driver.find_elements_by_xpath(
                    #     "//span[@class='block dark-grey-500 type-12 type-14-md lh3-lg']/span[@class='inline-block-sm hide']/span[@class='money']")[
                    #     1].text.split(" ")[1].replace(',', '')
                    #
                    # goal_val = int(goal_val)
                    # pledge_val = int(pledge_val)


                else:
                    ## if project is successful
                    # check if project is ongoing
                    prj_ongoing = self.new_driver.find_elements_by_xpath(
                        "//div[@class='ml5 ml0-lg']/div/div/span[@class='block type-16 type-28-md bold dark-grey-500']")
                    prj_end_soon = self.new_driver.find_elements_by_xpath(
                        "//div[@class='ml5 ml0-lg']/div/div/span[@class='block type-16 type-28-md bold red-400']")

                    if len(prj_ongoing) != 0 or len(prj_end_soon) != 0:
                        # if project is ongoing
                        loc = self.new_driver.find_elements_by_xpath(
                            "//div[@class='py2 py3-lg flex items-center auto-scroll-x']/a['nowrap navy-700 flex items-center medium mr3 type-12 keyboard-focusable']/span[@class='ml1']")
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
                        # get_pledge = self.new_driver.find_element_by_xpath("//div[@class='mb3']/div[@class='type-12 medium navy-500']/span[@class='money']").text
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

                        # get money
                        # goal_val = int(get_money_sp[1].replace(',', ''))
                        # pledge_val = int(get_pledge.split(" ")[1].replace(',', ''))

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

        res_dct_pass = {'state': ['success'],
                        'backers': [backers],
                        'pledged': [pledged],
                        'goal': [goal],
                        'launched': [launched],
                        'deadline': [deadline],
                        'currency_type': [currency_t]}

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

        res_dct_fail ={'state':['fail'],
                       'backers': [backers],
                       'pledged': [pledged],
                       'goal': [goal],
                       'launched': [launched],
                       'deadline': [deadline],
                       'currency_type': [currency_t]}

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

            ## COMMON
            prj_list = self.driver.find_elements_by_xpath("//div[@class='project-infobox']")
            prj_length = len(prj_list)

            for i in range(prj_length):
                print(">> Collecting prioject",i,"right now...")
                x = prj_list[i]
                p1 = x.find_element_by_xpath("h2/a")
                detail_url = p1.get_attribute("href")

                ## TITLE
                name = p1.text

                ## BLURB
                blurb = x.find_element_by_xpath("div[not(@class)]").text

                # if blurb is not empty
                if blurb != "":
                    ## CATEGORY
                    cat = x.find_element_by_xpath("div[@class='project-cat']")
                    cat_lst = cat.find_elements_by_tag_name("a")
                    category = cat_lst[0].text

                    ## PROJECT INFORMATION
                    info = x.find_element_by_xpath("div[@class='project-infobits']/div[@class='project-details']")
                    prj_info = info.text

                    # finding rate
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
                        main_dct.update(collect) # merging results
                        print(main_dct)
                        dfx = pd.DataFrame(main_dct)
                        blurb_df = blurb_df.append(dfx, sort=False)


        print("==================================")
        print("!COMPLETED!")
        print("==================================")
        print("Completed in {} seconds...".format(round(time.time() - self.timestart),2))

    def quitWeb(self):
        qt = self.driver.close()
        return qt

# EXAMPLE
# a = KicktraqCrawl()
# a.webcrawl(1,2,"dayone")