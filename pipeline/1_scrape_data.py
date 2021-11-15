#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Call scraping scripts and run in order
"""
from scraping_helpers.tea_scraping import scrape_teas
from scraping_helpers.reviews_scraping import scrape_reviews

print("Scraping Teas~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# scrape_teas()
print("Scraping Teas Complete")

print("Scraping Reviews~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
scrape_reviews()
print("Scraping Reviews Complete")