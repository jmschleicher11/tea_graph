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
import glob
import os

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
def scrape_reviews():
    for i in range(1,2):
        # time.sleep(50*random())

        url = review_url_string_1+str(i)+review_url_string_2
        driver = webdriver.Chrome(executable_path='../chromedriver')
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        reviews_json = convert_soup_to_json(soup)

        f = open(os.path.join('../data/reviews_separate_pages/', 'review_page_{}.json'.format(i)), 'w')
        f.write(reviews_json)
        f.close()

def combine_reviews():
    """ Read the separate json files for each of the review pages and combine into single file"""
    all_reviews = {}
    file_list = glob.glob('../data/reviews_separate_pages/*.json')
    for file in file_list:
        with open(file) as json_file:
            all_reviews.update(json.load(json_file))

    with open('../data/all_reviews.json', 'w') as reviews_file:
        json.dump(all_reviews, reviews_file)
