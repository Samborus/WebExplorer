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
import datetime
import json
import pickle

class Logger:
    def __init__(self, logfilePath):
        self.logfilePath = logfilePath
    def Info(self, message, data):
        pass
"""
dziwne
"""

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
        # assert self.cfg['SiteName'] in browser.title
        self.links.append(browser.current_url)
        timePoint = datetime.datetime.now() - timePoint
        self.printOpt('browser.get | End | ' + str(timePoint))
        timePoint = datetime.datetime.now()
        self.printOpt('find_elements | Start | ' + str(timePoint))
        self.research.elementsList = browser.find_elements_by_tag_name(self.cfg['Tag']);        
        timePoint = datetime.datetime.now() - timePoint
        self.printOpt('find_elements | End | ' + str(timePoint))
        len1 = self.research.elementsList.__len__()
        # pozycja = int(len1 / 3)
        # self.printOpt('losowy element nr ' + str(pozycja) + '/' + str(len1) + '\r\n' + 
        #     self.research.elementsList[pozycja].get_attribute('innerHTML')[:100].strip())        
        self.SaveToFile()
        browser.close()
        pass

    def ProcessElement(self, elem):
        procElem = Element()
        procElem.locationX = elem.location['x']
        procElem.locationY = elem.location['y']
        procElem.Childrencount = int(elem.get_attribute('childElementCount'))
        if procElem.Childrencount > 0 or (locationX  == 0 and procElem.locationY == 0):
            return None        
        
        procElem.innerHtml = elem.get_attribute('innerHTML').strip()
        if procElem.innerHtml == '':
            return None

        procElem.tagName = elem.tag_name
        procElem.innerText = elem.get_attribute('innerText').strip().lower()        
        procElem.className = elem.get_attribute('className').lower()
        if procElem.tagName == 'a':
            procElem.href = elem.get_attribute('href').strip()
            if self.cfg['Domain'] in procElem.href and '#' not in procElem.href:
                if procElem.href not in self.links:
                    self.links.append(procElem.href)        
        if '%' in procElem.innerText:
            procElem.hasPercantage = True
        if 'zł' in procElem.innerText or 'pln' in procElem.innerText or 'zł' in procElem.innerText:
            procElem.hasCurrencySIgn = True

        procElem.hasNumber = any(char.isdigit() for char in procElem.innerText)
        procElem.hasPriceInName = 'price' in procElem.className
        if procElem.tagName == 'a' and procElem.href != '':
            procElem.isLink = True

        return procElem
        
    def SaveToFile(self):
        len1 = self.research.elementsList.__len__()
        timePoint = datetime.datetime.now()
        self.printOpt('SaveToFile | Start | ' + str(timePoint))
        f = open('logs/' + str(timePoint) + '.csv', 'w+')
        f.write("tagName;className;locationX;locationY;isLink;hasCurrencySIgn;hasPercantage;hasNumber;hasPriceInName;innerText[:100]" + '\r\n')
        for i in range(len1 -1):
            try:
                tempEmelent = self.ProcessElement(self.research.elementsList[i])
                if tempEmelent is not None: 
                    self.research.ExtractedElements.append(tempEmelent)
                    
                    f.write(tempEmelent.tagName + ';' + str(tempEmelent.className) + ';' + 
                    str(tempEmelent.locationX) + ';' + str(tempEmelent.locationY) + ';' + 
                    str(tempEmelent.isLink) + ';' + 
                    str(tempEmelent.hasCurrencySIgn) + ';' + str(tempEmelent.hasPercantage) + ';' + 
                    str(tempEmelent.hasNumber) + ';' + str(tempEmelent.hasPriceInName) + ';' +
                        tempEmelent.innerText[:100] + '\r\n')
            except:
                self.printOpt('error\r\n')

        f.close()
        timePoint = datetime.datetime.now() - timePoint
        self.printOpt('SaveToFile | End | ' + str(timePoint))
        stdsc = StandardScaler()
        X_train_std = stdsc.fit_transform(self.research.ExtractedElements)
        X_test_std = stdsc.transform(self.research.ExtractedElements)
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

    