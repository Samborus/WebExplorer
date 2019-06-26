from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import datetime
import json

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
    hasChildren = False
    tagName = ''
    innerHtml = ''
    innerText = ''
    href = ''
    
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
        pozycja = int(len1 / 3)
        self.printOpt('losowy element nr ' + str(pozycja) + '/' + str(len1) + '\r\n' + 
            self.research.elementsList[pozycja].get_attribute('innerHTML')[:100].strip())        
        self.SaveToFile()
        browser.close()
        pass

    def ProcessElement(self, elem):
        procElem = Element()
        procElem.tagName = elem.tag_name
        procElem.innerHtml = elem.get_attribute('innerHTML').strip()
        procElem.innerText = elem.get_attribute('innerText').strip()        
        if procElem.tagName == 'a':
            procElem.href = elem.get_attribute('href').strip()
            if self.cfg['Domain'] in procElem.href and '#' not in procElem.href:
                if procElem.href not in self.links:
                    self.links.append(procElem.href)
        nestedElements = elem.find_elements_by_tag_name('*')
        procElem.hasChildren = nestedElements.__len__() > 0
        return procElem
        
    def SaveToFile(self):
        len1 = self.research.elementsList.__len__()
        timePoint = datetime.datetime.now()
        self.printOpt('SaveToFile | Start | ' + str(timePoint))
        f = open('logs/log_' + str(timePoint) + '.txt', 'w+')
        
        for i in range(len1 -1):
            try:
                # f.write(str(self.research.elementsList[i].get_attribute('innerHTML') + "\r\n"))
                tempEmelent = self.ProcessElement(self.research.elementsList[i])
                self.research.ExtractedElements.append(tempEmelent)
                # self.printOpt(elem.tagName)
                f.write(tempEmelent.tagName + ';' + str(tempEmelent.hasChildren) + ';' + tempEmelent.innerText[:100] + '\r\n')
            except:
                self.printOpt('error\r\n')

        f.close()
        timePoint = datetime.datetime.now() - timePoint
        self.printOpt('SaveToFile | End | ' + str(timePoint))

    def printOpt(self, text):
        if self.verbose:
            print(text)
    