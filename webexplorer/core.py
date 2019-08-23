from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json
import pickle
import pandas as pd

class Logger:
    def __init__(self, logfilePath):
        self.logfilePath = logfilePath
    def Info(self, message, data):
        pass

class Config:
    def __init__(self, confgfilePath):
        self.confgfilePath = confgfilePath
        self.data = None
    
    def GetConfiguration(self):
        if self.data is None:
            with open(self.confgfilePath) as json_file:  
                self.data = json.load(json_file)
        return self.data

class AppContext(Logger, Config):
    def __init__(self, confgfilePath):        
        Config.__init__(self, confgfilePath) 
        Logger.__init__(self, '/log/')
    pass

class Element:
    tagName = ''
    innerHtml = ''
    innerText = ''
    href = ''
    locationX = 0
    locationY = 0
    className = ''
    hasCurrencySIgn = False
    hasPercantage = False
    hasNumber = False
    hasPriceInName = False
    isLink = False
    cssFontSize = ''
    cssFontStyle = ''    
    cssFontWidth = ''
    cssFontColor = ''
    cssFontWeight = ''
    cssBgColor = ''
    cssHeight = ''
    
class Research:
    def __init__(self):
        self.startDate = datetime.datetime.now()
        self.error = ''
        self.elementsList = []
        self.ExtractedElements = []

class WebExplorer:    
    def __init__(self, appContext, verbose = False):
        self.appContext = appContext
        self.verbose = verbose
        self.research = Research()
        self.cfg = self.appContext.GetConfiguration()
        self.links = []        

    def Go(self):
        opts = Options()
        opts.set_headless()
        assert opts.headless

        timePoint = datetime.datetime.now()
        self.printOpt('browser.get | Start | ' + str(timePoint))
        browser = Firefox(options=opts)
        browser.get(self.cfg['Url'])
        self.links.append(browser.current_url)
        timePoint = datetime.datetime.now() - timePoint
        self.printOpt('browser.get | End | ' + str(timePoint))
        timePoint = datetime.datetime.now()
        self.printOpt('find_elements | Start | ' + str(timePoint))
        self.research.elementsList = browser.find_elements_by_tag_name('*');        
        timePoint = datetime.datetime.now() - timePoint
        self.printOpt('find_elements | End | ' + str(timePoint))
        
        self.ProcessElements()
        self.preprocess()
        self.writeCsv()
        browser.close()
        pass

    def GoCSV(self):
        df = pd.read_csv('df.csv')
        self.preprocess(df)
        pass

    def ProcessElement(self, elem):
        procElem = Element()
        procElem.locationX = elem.location['x']
        procElem.locationY = elem.location['y']
        childrencount = int(elem.get_attribute('childElementCount').strip())
        if childrencount > 0 or (procElem.locationX  == 0 and procElem.locationY == 0):
            return None        
        
        procElem.innerHtml = elem.get_attribute('innerHTML').strip()
        if procElem.innerHtml == '':
            return None

        procElem.tagName = elem.tag_name
        procElem.innerText = elem.get_attribute('innerText').strip().lower()        
        procElem.className = 'class ' + elem.get_attribute('className').strip().replace('\n','').replace('\t','').lower()
        if procElem.tagName == 'a':
            procElem.href = elem.get_attribute('href').strip()
            if self.cfg['Domain'] in procElem.href and '#' not in procElem.href:
                if procElem.href not in self.links:
                    self.links.append(procElem.href)        
        if '%' in procElem.innerText:
            procElem.hasPercantage = True
        else: 
            procElem.hasPercantage = False

        if 'zł' in procElem.innerText or 'pln' in procElem.innerText or 'zł' in procElem.innerText:
            procElem.hasCurrencySIgn = True
        else:
            procElem.hasCurrencySIgn = False

        procElem.hasNumber = any(char.isdigit() for char in procElem.innerText)
        procElem.hasPriceInName = 'price' in procElem.className
        if procElem.tagName == 'a' and procElem.href != '':
            procElem.isLink = True

        procElem.cssFontSize = elem.value_of_css_property('font-size')
        procElem.cssFontStyle = elem.value_of_css_property('font-style')
        procElem.cssFontWidth = elem.value_of_css_property('width')
        procElem.cssFontColor = elem.value_of_css_property('color')
        procElem.cssFontWeight = elem.value_of_css_property('font-weight')        
        procElem.cssBgColor = elem.value_of_css_property('background-color')
        procElem.cssHeight = elem.value_of_css_property('height')
        return procElem
        
    def ProcessElements(self):
        len1 = self.research.elementsList.__len__()    
        self.df = pd.DataFrame()            
        for i in range(len1 -1):
            try:
                tempEmelent = self.ProcessElement(self.research.elementsList[i])
                if tempEmelent is not None: 
                    self.research.ExtractedElements.append(tempEmelent)                
            except:
                self.printOpt('error\r\n')                

    def writeCsv(self):
        timePoint = datetime.datetime.now()
        self.printOpt('ProcessElements | Start | ' + str(timePoint))
        f = open('logs/' + str(timePoint) + '.csv', 'w+')
        f.write("tagName;className;locationX;locationY;isLink;hasCurrencySIgn;hasPercantage;hasNumber;hasPriceInName;innerText[:100]" + '\r\n')
        for tempEmelent in self.research.ExtractedElements:
            try:
                f.write(tempEmelent.tagName + ';' + str(tempEmelent.className) + ';' + 
                str(tempEmelent.locationX) + ';' + str(tempEmelent.locationY) + ';' + 
                str(tempEmelent.isLink) + ';' + 
                str(tempEmelent.hasCurrencySIgn) + ';' + str(tempEmelent.hasPercantage) + ';' + 
                str(tempEmelent.hasNumber) + ';' + str(tempEmelent.hasPriceInName) + ';' +
                    tempEmelent.innerText[:100].replace('"','') + '\r\n')
            except:
                self.printOpt('error write \r\n')
        f.close()
        timePoint = datetime.datetime.now() - timePoint
        self.printOpt('ProcessElements | End | ' + str(timePoint))
        pass

    def preprocess(self, df = None):
        if df is None:
            df = pd.DataFrame(data = [vars(s) for s in self.research.ExtractedElements], 
                columns = ['tagName', 'innerHtml','innerText','href','locationX','locationY','className',
                            'hasCurrencySIgn','hasPercantage','hasNumber','hasPriceInName','isLink',
                            'cssFontSize', 'cssFontStyle', 'cssFontWidth','cssFontColor','cssFontWeight',
                            'cssBgColor','cssHeight',])
            df.to_csv('df.csv')
        else:
            del df['Unnamed: 0']

        del df['innerHtml']
        del df['innerText']
        del df['href']

        classMapping = {label: idx for idx, label in enumerate(np.unique(df['className'])) }
        tagMapping = {label: idx for idx, label in enumerate(np.unique(df['tagName'])) }
        cssFontSize = {label: idx for idx, label in enumerate(np.unique(df['cssFontSize'])) }
        cssFontStyle = {label: idx for idx, label in enumerate(np.unique(df['cssFontStyle'])) }
        cssFontWidth = {label: idx for idx, label in enumerate(np.unique(df['cssFontWidth'])) }
        cssFontColor = {label: idx for idx, label in enumerate(np.unique(df['cssFontColor'])) }
        cssFontWeight = {label: idx for idx, label in enumerate(np.unique(df['cssFontWeight'])) }
        cssBgColor = {label: idx for idx, label in enumerate(np.unique(df['cssBgColor'])) }
        cssHeight = {label: idx for idx, label in enumerate(np.unique(df['cssHeight'])) }

        df['className'] = df['className'].map(classMapping)
        df['tagName'] = df['tagName'].map(tagMapping)
        df['cssFontSize'] = df['cssFontSize'].map(cssFontSize)
        df['cssFontStyle'] = df['cssFontStyle'].map(cssFontStyle)
        df['cssFontWidth'] = df['cssFontWidth'].map(cssFontWidth)
        df['cssFontColor'] = df['cssFontColor'].map(cssFontColor)
        df['cssFontWeight'] = df['cssFontWeight'].map(cssFontWeight)
        df['cssBgColor'] = df['cssBgColor'].map(cssBgColor)
        df['cssHeight'] = df['cssHeight'].map(cssHeight)
        df[['hasCurrencySIgn','hasPercantage','hasNumber','hasPriceInName','isLink']] *= 1

        sc = StandardScaler()
        sc.fit(df)
        X_train_std = sc.transform(df)

        pass

    def printOpt(self, text):
        if self.verbose:
            print(text)

    def SavePickle(self, obj):
        with open('outfile', 'wb') as fp:
            pickle.dump(obj, fp)

    def LoadPickle(self):
        with open ('outfile', 'rb') as fp:
            itemlist = pickle.load(fp)
        return itemlist

    