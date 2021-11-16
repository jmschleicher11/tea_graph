#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Call scraping scripts and run in order
"""
import sys
sys.path.append('../')

from scraping_helpers.tea_scraping import scrape_teas
from scraping_helpers.reviews_scraping import scrape_reviews, combine_reviews

print("Scraping Teas~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# scrape_teas()
print("Scraping Teas Complete")

print("Scraping Reviews~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# scrape_reviews()
print("Scraping Reviews Complete")

print("Combining Reviews~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
combine_reviews()
print("Reviews scraped and combined")