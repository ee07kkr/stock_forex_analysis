#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 20:59:55 2018
@author: Rewari
"""

import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from datetime import datetime 
import time
from pandas.tseries.offsets import BDay

end = datetime.today() 
baseUrl = 'https://finance.yahoo.com/quote/'
tech_list = ['AAPL','GOOG','MSFT','TSLA']

def getStockData(tick,endPeriod,businessDays):
    businessDaysSets = int(businessDays/100)
    for y in range(businessDaysSets):
        end = endPeriod - BDay(y*100+(y))
        start = end - BDay(100)
        unixStart = int(time.mktime(start.timetuple()))
        unixEnd = int(time.mktime(end.timetuple()))
        url_link =(baseUrl + str(tick) + '/history?period1=' + str(unixStart) + '&period2=' + str(unixEnd) + '&interval=1d&filter=history&frequency=1d')
        connect2Website(url_link)
def connect2Website(url):
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, "lxml")
    summary = soup.find('div',{'class':'Pb(10px) Ovx(a) W(100%)'})
    tables = summary.find_all('table')
    data = []
    rows  = tables[0].find_all('tr')
    for tr in rows:
        cols = tr.findAll('td')
        if len(cols) == 7:
            for td in cols:
                text = td.find(text=True)
                data.append(text)    
#   [expression for item in list if conditional] How to think of list comprehension
#    [data.remove(element) for element in data if '*' in element]
    dFrame = pd.DataFrame(np.array(data).reshape(int(len(data)/7),7))
    dFrame.columns=['Date','Open','High','Low','Close','Aclose','Volume']
    dFrame.set_index('Date',inplace=True)
    dump2csv(dFrame)
def dump2csv(dataFrame):
    filename = '/Users/krewari/Desktop/'+ str(stock) +'.csv'
    if os.path.exists(filename):
       append_write = 'a'
       dataFrame.to_csv(filename,sep='\t',mode=append_write,header = False)
    else:
        append_write = 'w'
        dataFrame.to_csv(filename,sep='\t',mode=append_write)
for stock in tech_list:
    getStockData(stock,end,300)
    