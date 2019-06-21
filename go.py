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
    
class Research:
    def __init__(self):
        self.startDate = datetime.datetime.now()
        self.error = ''
        self.elementsList = None
        self.ExtractedElements = []

class WebExplorer:    
    def __init__(self, appContext, verbose = False):
        self.appContext = appContext
        self.verbose = verbose
        self.research = Research()
        self.cfg = self.appContext.GetConfiguration()

    def Go(self):
        opts = Options()
        opts.set_headless()
        assert opts.headless
        startTime = datetime.datetime.now()
        self.printOpt(startTime)

        browser = Firefox(options=opts)
        browser.get(self.cfg['Url'])
        # assert self.cfg['SiteName'] in browser.title

        self.research.elementsList = browser.find_elements_by_tag_name(self.cfg['Tag']);
        
        len1 = self.research.elementsList.__len__()
        # self.printOpt(self.research.elementsList[len1 % 3].get_attribute('innerHTML'))        
        self.SaveToFile()
        pass

    def ProcessElement(self, element):
        pass

    def SaveToFile(self):
        len1 = self.research.elementsList.__len__()
        self.printOpt('len = ' + str(len1))        
        now = datetime.datetime.now()
        self.printOpt(now)
        f = open(str(datetime.datetime.now()) + '.txt', 'w+')
        
        for i in range(len1 -1):
            try:
                # f.write(str(self.research.elementsList[i].get_attribute('innerHTML') + "\r\n"))
                elem = Element()
                elem.tagName = self.research.elementsList[i].tag_name
                elem.innerHtml = self.research.elementsList[i].get_attribute('innerHTML').strip()
                self.research.ExtractedElements.append(elem)
                self.printOpt(elem.tagName)
                f.write(str(elem.innerHtml))
            except:
                self.printOpt('error\r\n')
        f.close()

    def printOpt(self, text):
        if self.verbose:
            print(text)
pass

if __name__ == "__main__":    
    appContext = AppContext('config.cfg')
    program = WebExplorer(appContext, True).Go()
    pass
    
 


