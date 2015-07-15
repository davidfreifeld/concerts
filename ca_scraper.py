from bs4 import BeautifulSoup
import string
import re
from numpy import mean

class CAScraper():
    
    directory = 'C:/Users/David/workspace/concerts/data/'
            
    def __init__(self):
        pass
    
    def loadSingleHTML(self, csvFile, number = 0):
        
        """ First parse the html elements """
        htmlFile = open(self.directory + 'pages/capage' + str(number) + '.html') 
        soup = BeautifulSoup(htmlFile, "html.parser")
        tags = soup.find_all("tr", class_="greyBg")
        whiteTags = soup.find_all("tr", class_="whiteBg")
        tags.extend(whiteTags)
        
        """ Regular expressions for text parsing"""
        regDate = re.compile(r'[01][0-9]/[0-3][0-9]/[12][09][019][0-9]')
        regMainAct = re.compile(r'(.*?),(.*)')
        regVenue = re.compile(r'(.*)\s[-]\s(.*),\s(.*)$')
        regBlues = re.compile(r'Blues At The Crossroads: The Robert Johnson Centennial')
        regPeltier = re.compile(r'Bring Leonard Peltier Home in 2012')
        regWS = re.compile(r'A Night at Woodstock')
         
        csv = ''
        for row in tags:
            cols = row.find_all()
            for i in range(len(cols)):
                text = cols[i].text
                
                if (i == 0):
                    text = regDate.findall(text)[0] + ','
                     
                if (i == 1):
                    if regBlues.findall(text) or regPeltier.findall(text) or regWS.findall(text):
                        csv = csv[:-12]
                        break
                    if text[0] == '\"' and text[-2] == '\"':
                        text = text[1:-2].replace(',', '')
                    bandSplit = regMainAct.findall(text)
                    if bandSplit:
                        openers = ''
                        if len(bandSplit[0]) > 1:
                            openers = bandSplit[0][1].replace(',', ';').strip()
                        text = bandSplit[0][0].strip() + ',' + openers + ','
                    else:
                        text =  text.strip() + ',,'
                         
                if (i == 2):
                    venSplit = regVenue.findall(text)
                    venue = venSplit[0][0].replace(',', ';').strip()
                    city = venSplit[0][1].replace(',', '').strip()
                    text = venue + ',' + city + ',' + venSplit[0][2].strip() + ','
                     
                if (i == 3):
                    text = text.replace(',', ';').strip() + ','
                     
                if (i == 4 or i == 6):
                    text = text.replace(',', '').replace('/', ',').replace(' ', '') + ','
                     
                if (i == 5):
                    text = text.replace(',', '').replace('$', '').strip() + ','
                     
                if (i == 7):
                    text = str(float(text.replace('%', '')) / 100) + ','
                     
                if (i == 8):
                    tixPxs = text[1:].replace('$', ';').replace(',','')
                    nums = [float(tixPx) for tixPx in tixPxs.split(';')]
                    text = tixPxs.strip() + ',' + str(mean(nums))
                     
                csv = csv + text.replace('"', '\'')
            csv = csv + '\n'
      
        csv = filter(lambda x: x in string.printable, csv)
      
        csvFile.write(csv)
        
    
    def writeAllData(self, numAppend = ''):
        
        csvFile = open(self.directory + 'BoxOfficeData' + numAppend + '.csv', 'a')
        
        """ Write headers """
        csvFile.write('Date,Headliner,Openers,Venue,City,State,Promoter,SoldOutShows,TotalShows,Gross,Sold,Capacity,SoldRatio,TicketPrices,AvgPrice\n')
        
        for i in range(352):  #352 to run all data
            print('Loading file ' + str(i))
            self.loadSingleHTML(csvFile, i)
            
        csvFile.close()
    
foo = CAScraper()
foo.writeAllData('')