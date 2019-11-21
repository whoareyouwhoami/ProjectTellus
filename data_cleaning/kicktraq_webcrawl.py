"""
- 진행중인 프로젝트는 kickstarter 페이지에서 마치 unsuccessful 처럼 뜬다.
- 시간이 얼마 안남은 프로젝트는 시간이 줄어드는데 그 해당 class가 몇 분 남았다를 보여주는 class랑 똑같은지는 확인해야됨.
- 아니면 이거 돌리는 시간을 오후 6시 마다 돌리는 거로 둔다.

"""

## 시간 감소하는 클래스
# ml5 ml0-lg
# span -> block type-16 type-28-md bold red-400


import os
import re
import pandas as pd
import numpy as np
import requests
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys

pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

path = os.getcwd()
driver = wd.Chrome(path + '/chromedriver')

# DataFrame for result
blurb_df = pd.DataFrame(columns = ['name', 'blurb', 'state', 'category',
                                   'funding_rate', 'pledged', 'goal','currency_type',
                                   'launched', 'deadline'])


success_currency = {'AU$': 'AUD', 'CA$': 'CAD', 'HK$': 'HKD', 'MX$': 'MXN', 'NZ$': 'NZD', 'US$': 'USD', 'S$': 'SGD'}

unsuccess_currency = {'Australia': 'AUD', 'Canada': 'CAD', 'Hong Kong': 'HKD', 'Mexico': 'MXN', 'NZ': 'NZD', 'Singapore': 'SGD'}


def get_currency_type(currency_symb, detail_url):
    global currency_type
    """
    get rate for `kr` and `$` to USD
 
    """
    driverx = wd.Chrome(path + '/chromedriver')
    driverx.get(detail_url)
    content = driverx.find_element_by_xpath("//div[@id='project-info-text']")
    content_lst = content.text.split('\n')

    funding_lst = [s for s in content_lst if "Funding:" in s]
    funding_goal = funding_lst[0].split(" of ")[1]

    if currency_symb == 'k':
        currency_type = funding_goal.split(" ")[1]  # get country for `kr` currency


    else:  # for `$`
        content = driverx.find_element_by_id('button-backthis')
        prj_addr = content.get_attribute("href")
        new_driver = wd.Chrome(path + '/chromedriver')
        new_driver.get(prj_addr)

        ## check if project is successful or not
        check_content = new_driver.find_elements_by_xpath("//div[@id='hidden_project']")
        if len(check_content) != 0:
            currency_type = "USD (*)"
        else:
            prj_status = new_driver.find_elements_by_xpath("div[(@class='normal type-18')]")
            if len(prj_status) != 0:
                # if project is unsuccessful
                # get location
                location = new_driver.find_elements_by_xpath(
                    "//div[@class='py2 py3-lg flex items-center auto-scroll-x']/a['nowrap navy-700 flex items-center medium mr3 type-12 keyboard-focusable']/span[@class='ml1']")[
                    3].text
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
                # if project is successful

                # check if project is ongoing
                prj_ongoing = new_driver.find_elements_by_xpath("//div[@class='ml5 ml0-lg']/span[@class='block type-16 type-28-md bold dark-grey-500']")
                if len(prj_ongoing) != 0:
                    # if project is ongoing
                    loc = new_driver.find_elements_by_xpath("//div[@class='py2 py3-lg flex items-center auto-scroll-x']/a['nowrap navy-700 flex items-center medium mr3 type-12 keyboard-focusable']/span[@class='ml1']")[3].text
                    loc_lst = len(loc)
                    location = loc[loc_lst]
                    region = location.split(",")[1].strip()

                    # get currency
                    if region in unsuccess_currency:
                        currency_type = unsuccess_currency[region]
                    else:
                        currency_type = "USD"


                else:
                    # if project is successful and done
                    get_pledge = new_driver.find_element_by_xpath("//div[@class='mb3']/div[@class='type-12 medium navy-500']/span[@class='money']").text
                    get_money = new_driver.find_element_by_xpath("//div[@class='mb3']/h3[@class='mb0']/span[@class='money']").text


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

        new_driver.close()
    driverx.back()
    return currency_type


def webcrawl(start, end):
    global blurb_df
    for page in range(start,end+1):
        print("==================================")
        print("Collecting page",page,"......")
        print("==================================")

        # load page
        driver.get('https://www.kicktraq.com/dayones/?page={}'.format(page))

        # get list of all project list and info
        prj_list = driver.find_elements_by_xpath("//div[@class='project-infobox']")
        prj_length = len(prj_list)

        for i in range(prj_length):
            print(">> Collecting project",i,"right now...")
            x = prj_list[i]
            p1 = x.find_element_by_xpath("h2/a")

            ## TITLE
            name = p1.text

            ## BLURB
            blurb = x.find_element_by_xpath("div[not(@class)]").text

            ## CATEGORY
            cat =  x.find_element_by_xpath("div[@class='project-cat']")
            cat_lst = cat.find_elements_by_tag_name("a")
            category = cat_lst[0].text

            ## PROJECT INFORMATION
            info = x.find_element_by_xpath("div[@class='project-infobits']/div[@class='project-details']")
            prj_info = info.text

            # finding rate
            rate_info = info.find_element_by_tag_name("span").text
            percent = int(re.findall('\d+', rate_info)[0])

            if percent >= 100:
                pledged = prj_info.split('\n')[1].split(': ')[1].split(' of ')[0]
                goal = prj_info.split('\n')[1].split(': ')[1].split(' of ')[1].split(' (')[0]
                year = prj_info.split('\n')[3].split('(')[1][:-1]
                launched = prj_info.split('\n')[3].split(": ")[1].split(' -> ')[0]
                deadline = prj_info.split('\n')[3].split(": ")[1].split(' -> ')[1].split(' (')[0]


                # finding currency
                currency_symb = goal[0]

                if currency_symb == '$' or currency_symb == 'k':
                    detail_url = p1.get_attribute("href")
                    currency_symb = get_currency_type(currency_symb, detail_url)

                row = [name, blurb, 'success', category, percent, pledged, goal, currency_symb, year + ' ' + launched,
                       year + ' ' + deadline]


                blurb_df = blurb_df.append(pd.Series(row, index=['name', 'blurb', 'state', 'category', 'funding_rate', 'pledged', 'goal','currency_type', 'launched', 'deadline']), ignore_index=True)

    driver.close()
    print("==================================")
    print("!COMPLETED!")
    print("==================================")