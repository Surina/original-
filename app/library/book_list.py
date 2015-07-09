# -*- coding: utf-8 -*-
import requests
import HTMLParser  
import urlparse  
import string  
import re  
import datetime 

class book_list:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        self.proxies = {
                  "http": "http://219.217.180.1:808"
                        }

        self.login_url = 'http://portal.dlnu.edu.cn/Login'
        self.getdata_url= 'http://portal.dlnu.edu.cn/mhpd/jtsy/main_xs.jsp'

        self.headers = {#'Host': 'portal.dlnu.edu.cn',
                        #'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0',
                        #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        #'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate',
                        }

        self.s = requests.Session()

        
    def login(self):
        self.postdata = {
            'userName': self.username,
            'password': self.password
           }

        
        self.s.post(self.login_url, self.postdata, headers = self.headers)
        


    def get_data(self):
        k = self.s.get(self.getdata_url, headers = self.headers)
        self.text = k.text

    def deal_data(self):

        book =[]
        items = re.findall('<td  width="240"  height="25" align="left">(.*?)</td>.*?<td width="70" align="center">(\d{4}-\d{2}-\d{2})        </td>', self.text, re.S)
        if items == []:
            return u'无借阅信息'
        else:
            
            for item in items:
                row = u'\n%s  到期时间: %s'% (item[0], item[1])
                book.append(row)
            book = ''.join(book)
            return book

