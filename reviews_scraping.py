#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 07:02:21 2021

@author: Floreana
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from random import random
import json

from url_file import review_url_string_1, review_url_string_2

def convert_soup_to_json(parsed_soup):
    """ Converts review soup object from parsed html to a usable dictionary as json"""

    reviews_string = str(parsed_soup.body.string)
    reviews_extra = json.loads(reviews_string)
    reviews_list = reviews_extra['data']

    ## Current reviews_list is a list of dictionaries; convert to dict with review ID as key
    reviews_dict = dict()
    for review in reviews_list:
        review_id = review['id']
        if review_id in reviews_dict.keys():
            print(review_id)
        else:
            reviews_dict[review_id] = review

    return json.dumps(reviews_dict)

## The reviews page has an API call that is triggered by clicking the next button. Using Selenium
## to iterate through the 100 pages of reviews and saving each page's reviews as a json dictionary.
for i in range(1,101):
    time.sleep(50*random())

    url = review_url_string_1+str(i)+review_url_string_2
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    reviews_json = convert_soup_to_json(soup)

    f = open('data/reviews_separate_pages/review_page_{}.json'.format(i), 'w')
    f.write(reviews_json)
    f.close()
