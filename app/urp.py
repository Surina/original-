# coding=utf-8
import requests
import HTMLParser  
import urlparse  
import string  
import re  
import datetime 
from bs4 import BeautifulSoup


class urp:

    

    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        self.proxies = {
                  "http": "http://219.217.180.1:808"
                        }

        self.login_url = 'http://zhjw.dlnu.edu.cn/loginAction.do'
        self.get_fulldata_url= 'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
        self.get_recentdata_url= 'http://zhjw.dlnu.edu.cn/bxqcjcxAction.do'
        
        self.get_evaluation_url ='http://zhjw.dlnu.edu.cn/jxpgXsAction.do?oper=listWj'
        self.open_evaluation_url ='http://zhjw.dlnu.edu.cn/jxpgXsAction.do'
        self.post_evaluation_data_url ='http://zhjw.dlnu.edu.cn/jxpgXsAction.do?oper=wjpg'
        
        self.headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept': 'application/x-www-form-urlencoded',

                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                    'Accept-Encoding':    'gzip, deflate',
                    'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
                        }  

        self.s = requests.Session()

        
    def login(self):
        postdata = {
                        'zjh' : self.username,
                        'mm' : self.password
                        }

        
        r = self.s.post(self.login_url, postdata, headers = self.headers)
        if len(r.text) == 489:
            return True
        else:
            return False
            
            

    def get_fulldata(self):
        req = self.s.get(self.get_fulldata_url)
        text = req.text
        soup = BeautifulSoup(text)
        tag = soup.find('iframe')
        url_fulldata = 'http://zhjw.dlnu.edu.cn/' + tag['src']
        req = self.s.get(url_fulldata)
        text = req.text
        garde =[]
        items = re.findall('<tr.*?<td align="center">.*?<td align="center">.*?<td align="center">(.*?)</td>.*?<p align="center">(.+?)&nbsp;</P>.*?</td>.*?</tr>', text, re.S)
        if items == []:
            return u'无最近考试信息'
        else:
            for item in items:
                row = u'%s  %s'% (string.strip(item[0]), string.strip(item[1]))
                garde.append(row)
            garde = '\n'.join(garde)
            return garde




    def get_recentdata(self):
        data = []
        req = self.s.get(self.get_recentdata_url, headers = self.headers)
        text = req.text
        soup = BeautifulSoup(text)
        courses = soup.find_all('tr', onmouseout="this.className='even';")
        if courses == []:
            return u'无最近考试信息'
        else:
            for course in courses:
                name = course.find('td').find_next_sibling('td').find_next_sibling('td')
                grade = name.find_next_sibling('td').find_next_sibling('td').find_next_sibling('td').find_next_sibling('td')
                name = string.strip(name.string)
                grade = string.strip(grade.string)
                if len(grade) != 0:
                    row = u'%s  %s'% (name, grade)
                    data.append(row)
            data = '\n'.join(data)
            if  len(data) == 0:
                return u'无最近考试成绩'
            else:
                return data

    def open_evaluation(self, wjbm, bpr, pgnr):
        self.wjbm = wjbm
        self.bpr = bpr
        self.pgnr = pgnr
        postdata = {
                    'wjbm': self.wjbm,
                    'bpr': self.bpr,
                    'pgnr': self.pgnr,
                    'oper': 'wjShow',
                    'wjmc': '',
                    'bprm': '',
                    'pgnrm': '',
                    'pageSize': '20',
                    'page': '1',
                    'currentPage': '1',
                    'pageNo': ''
                    }
        self.s.post(self.open_evaluation_url, data = postdata)

    def postevaluation(self):
        postdata = {
                    'wjbm': self.wjbm,
                    'bpr': self.bpr,
                    'pgnr': self.pgnr,
                    '0000000133': '6_1',
                    '0000000135': '6_1',
                    '0000000160': '4_1',
                    '0000000163': '4_1',
                    '0000000166': '5_1',
                    '0000000190': '5_1',
                    '0000000192': '5_1',
                    '0000000193': '5_1',
                    '0000000194': '8_1',
                    '0000000195': '5_1',
                    '0000000196': '5_1',
                    '0000000197': '5_1',
                    '0000000198': '10_1',
                    '0000000199': '10_1',
                    '0000000200': '7_1',
                    '0000000201': '8_1',
                    'zgpj' : u'老师不错'.encode('gbk')
                    }
        self.s.post(self.post_evaluation_data_url, data = postdata)

    def evaluation(self):

        req = self.s.get(self.get_evaluation_url)
        text = req.text
        soup= BeautifulSoup(text)
        soup = soup.find_all('img', align = "center")
        for litem in soup:
            s =  litem['name'].split('#@')
            self.open_evaluation(s[0], s[1], s[-1])
            self.postevaluation()

