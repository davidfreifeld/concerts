from selenium import webdriver

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import time
import random

class CASaver():
    
    url = "http://celebrityaccess.com/members/boxoffice/bosearchform.php"
    username = "pr037283 "
    dailyPass = "alpha"
    ffDriver = None
    counter = 0;
    itemsScraped = 0
    def __init__(self):
        """
        
            Args:
                dailyP: daily password, if None defaults to value of 2015-6-23
        """
        #if(dailyP is not None):
        #    self.dailyPass = dailyP
        #self.itemsScraped = itemsScrapedStart
        self.ffDriver = webdriver.Chrome('C:/Users/David/workspace/concerts/chromedriver/chromedriver')
            
            
    def Login(self):
        self.ffDriver.get("http://celebrityaccess.com/login.php")
        self.ffDriver.find_element_by_name("userName").clear()
        self.ffDriver.find_element_by_name("userName").send_keys("pr037283")
        self.ffDriver.find_element_by_name("password").send_keys("david")
        self.ffDriver.find_element_by_name("dPassword").send_keys("alpha")
        # ERROR: Caught exception [unknown command []]
        self.ffDriver.find_element_by_name("login").click()
        
    def SearchForBoxOffice(self):
        self.ffDriver.get("http://celebrityaccess.com/members/boxoffice/bosearchform.php")
        self.ffDriver.find_element_by_name("tdStart").send_keys("01/01/1970")
        self.ffDriver.find_element_by_name("tdEnd").send_keys("06/23/2015")
        self.ffDriver.find_elements_by_xpath('//select/option[@value="0"]')[1].click()
        self.ffDriver.find_elements_by_xpath('//input[@name="gogetit" and @value="Search"]')[1].click()
    
    def SavePage(self):
        srcCode = self.ffDriver.page_source.encode('utf-8')
        filename = "capage" + str(self.counter) + ".html"
        pageFile = open('C:/Users/David/workspace/concerts/data/pages/' + filename,'w') 
        pageFile.write(srcCode)
        pageFile.close()
        self.counter +=1
    
    def LoadNextBOResults(self):
        self.ffDriver.find_element_by_xpath("//a[contains(text(),'Next Page')]").click()
    
    def Run(self):
        self.Login()
        self.SearchForBoxOffice()
        while(self.itemsScraped < 1760000 ):
            self.SavePage()
            self.itemsScraped += 500
            waitTime = 30
            print "scraped " + str(self.itemsScraped)
            print "waiting " + str(waitTime)
            time.sleep(waitTime)
            self.LoadNextBOResults()
    
    
        
foo = CASaver()   
foo.Run()        