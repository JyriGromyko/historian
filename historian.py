#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import selenium
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


import time
import datetime

import plotly
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import sqlalchemy
import json

import requests
import numpy as np
import statsmodels.api as sm
import copy
import random
import os
import webbrowser
import logging
from logging.handlers import RotatingFileHandler


# In[ ]:

options = Options()
options.headless = True
options.binary_location='/usr/bin/google-chrome/chrome.exe'
driver = webdriver.Chrome(chrome_options = options,executable_path='/home/ec2-user/')
driver.get("https://www.dailyfx.com/gold-price")

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
fname = "GOLD.log"
logging.basicConfig(filename = fname,
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.ERROR)

logger = logging.getLogger()
handler = RotatingFileHandler(fname, maxBytes=100024, backupCount=1)
logger.addHandler(handler)


# In[ ]:


timestamp = datetime.datetime.now()
def update_gold(timestamp):
    link = driver.find_element(By.CSS_SELECTOR, "div.dfx-technicalSentimentCard__netLongContainer > span")
    price__data = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#dfx-instrumentPageBar-GC > div.d-inline-flex.flex-column.dfx-border--a-1.w-100 > div > div.dfx-singleInstrument.col-lg-5.dfx-border--b-1.dfx-border--b-lg-0.text-nowrap.p-2.mb-lg-0.dfx-border--b-lg-0.dfx-border--r-lg-1 > div.jsdfx-singleInstrument__priceWrapper.d-flex.flex-column.h-100.justify-content-around > div.dfx-singleInstrument__price.dfx-rate.dfx-font-size-3.font-weight-bold.text-right"))
    )
    percentage = link.get_attribute("data-value")
    price = price__data.get_attribute("data-value")
    d = {'timestamp': [timestamp], 'percentage': [percentage], 'price': [price]}
    analytics = pd.DataFrame(data=d)
    return analytics

gold_frame = update_gold(timestamp)
print(gold_frame)
while True:        
        gold_frame = update_gold(timestamp)
        gold_engine = sqlalchemy.create_engine('sqlite:///gold.db')
        gold_frame.to_sql('gold', gold_engine, if_exists='append')
        analytics__data = pd.read_sql('gold', gold_engine)
        
        gold_fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add traces
        gold_fig.add_trace(
            go.Scatter(x = analytics__data['timestamp'],
            y=analytics__data['percentage'], name="Percentage"),
            secondary_y=False,
        )
        
        gold_fig.add_trace(
            go.Scatter(x = analytics__data['timestamp'],
            y=analytics__data['price'], name="Price"),
            secondary_y=False,
        )

        plotly.offline.plot(gold_fig,filename='gold.html',config={'displayModeBar': False}, auto_open=False)
        time.sleep(600) #900

