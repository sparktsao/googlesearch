#!/usr/bin/env python
import sys, pycurl
import StringIO as SIO2
import sys
from lxml import etree
import xml.etree.ElementTree as ET
from io import StringIO, BytesIO
import json
reload(sys)  
sys.setdefaultencoding('utf8')
useragent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'

class WebPage:
    def __init__(self):
        self.content = ''
        self.hitrule = []
        self.url = 'https://www.google.com.tw/search?q='

    def prune(self,query):
        querys = [x for(x) in query.split(" ") if len(x)>0]
        query = '+'.join(querys)
        return query

    def doquery(self,query):
        self.query = query

        import os.path
        if os.path.exists(query+".html"):
            self.content = open(query+".html").read()
            return self.content

        qurl = self.url+query+'&num=100'
        print qurl,'ok', type(qurl)

        buffer = SIO2.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, qurl)
        c.setopt(c.USERAGENT, useragent)
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()
        c.close()
        self.content = buffer.getvalue()
        return self.content

    def showpage(self):        
        parser = etree.HTMLParser()
        xpath1 = '//*[@id="rso"]/div/div'
        xpath2 = '//*[@id="rso"]/div[2]/div/div[1]/div/h3/a'
        xpath3 = '//*[@id="rso"]/div[2]/div/div[9]/div/div/div/span'
        tree = etree.parse(StringIO(unicode(self.content)),parser)
        for i,tr in enumerate(tree.xpath(xpath1)[0].getchildren()):        
            arr = tree.xpath('//*[@id="rso"]/div/div/div['+str(i+1)+']/div/h3/a')
            for j,_ in enumerate(arr):
                print arr[j].text
                print "---> url:", arr[0].attrib['href']
                desc = tree.xpath('//*[@id="rso"]/div/div/div['+str(i+1)+']/div/div/div/span')
                for k,_ in enumerate(desc):
                    print "---> sum:", desc[k].text

    def cache(self):
        f1 = open(self.query+".html","w")
        f1.write(self.content)
        f1.close()        

go = WebPage()
query = go.prune(sys.argv[1])
print query
content = go.doquery(query)
go.cache()
go.showpage() 



