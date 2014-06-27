import urllib2
import BeautifulSoup
import numpy as np
import datetime
import jdcal

class GetTransients:
    
    def __init__(self):
        #Hardcode the information for reading skyalert
        contenturl = "http://www.skyalert.org/events/table/0/"
        soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(contenturl).read())
        self.table = soup.find('table',attrs={'class': 'tablesorter'})

    def Update(self):
        contenturl = "http://www.skyalert.org/events/table/0/"
        soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(contenturl).read())
        self.table = soup.find('table',attrs={'class': 'tablesorter'})


    def ParseMagnitudes(self,mags):

        return np.random.normal(loc=19.6,scale=3.,size=len(mags))

        

    def ParseJulian(self,dates):

        jd = np.zeros(len(dates))
        for i,dt in enumerate(dates):
            yr,mn,other= dt.split('-')
            if float(yr) < 2000:
                yr = str(int(yr) + 2000)

            dy, other = other.split('T')
            hr,mt,sec = other.split(':')
            sec = sec[0:2]
            jd[i] = sum(jdcal.gcal2jd(yr,mn,dy)) + (float(hr)+float(mt)/60. + float(sec)/3600.)/24. 

        return jd

    def GetData(self):
        #Return the Ra,Dec,Mag,JD of SNR
        thisTable = self.table.findAll('tbody')
        rows = thisTable[0].findAll('tr')

        data = []
        for itr, tr in enumerate(rows):
            cols = tr.findAll('td')
            data.append ([cols[2].string,cols[3].string,cols[4].string])

        data = np.array( data )
        ra = data[:,0].astype('float')
        dec= data[:,1].astype('float')
        jd = self.ParseJulian(data[:,2])
        mags =  self.ParseMagnitudes(data[:,2])


        return ra, dec,mags, jd

