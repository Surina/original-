# coding=utf-8
import requests
from app import db
from models import User
from urp import urp
from book_list import book_list
from drcom import drcom

class checkevent:
    def __init__(self, fromuser):
        
        self.fromuser = fromuser
        self.exist_user = User.query.filter_by(openid = self.fromuser).first()


    def recentgrade(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            geturp = urp(self.exist_user.username, self.exist_user.password_urp)
            if geturp.login():
                grades = geturp.get_recentdata()
                return grades
            else:
                text = u'密码变化,请重新绑定'
                return text
                
    def fullgrade(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            geturp = urp(self.exist_user.username, self.exist_user.password_urp)
            if geturp.login():
                grades = geturp.get_fulldata()
                return grades
            else:
                text = u'密码变化,请重新绑定'
                return text
                
    def booklist(self):
        
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            geturp = urp(self.exist_user.username, self.exist_user.password_urp)
            if geturp.login():
                booklist = book_list(self.exist_user.username, self.exist_user.password_urp)
                booklist.login()
                booklist.get_data()
                booklist = booklist.deal_data()
                return booklist
            else:
                text = u'密码变化,请重新绑定'
                return text
            
    def binding(self):
        
        if self.exist_user is None:
            url = u'http://jzp113.ngrok.com/login?openid=' + self.fromuser
            href = u'<a href="%s">点我绑定</a>' %url
            return href
            
        else:
            text = u'您已绑定,如密码变化,请先解除绑定.'
            return text
            
    def drcom(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            getdrcom= drcom(self.exist_user.username, self.exist_user.password_drcom)
            if getdrcom.login():
                getdrcom.get_flow()
                getdrcom.get_date()
                flow_date = getdrcom.deal_data()
                return flow_date
            else:
                text = u'密码变化,请重新绑定'
                return text

    def drcom_logout(self):
        if self.exist_user is None:
            text = u'请绑定后使用'
            return text
        else:
            getdrcom= drcom(self.exist_user.username, self.exist_user.password_drcom)
            if getdrcom.login():
                getdrcom.logout()
                text = u'下线成功!'
                return text
            else:
                text = u'密码变化,请重新绑定'
                return text


    def key_check(self,key):
        lookup = {
            'binding': self.binding,
            #'unlock': self.unlock,
            'drcom_logout': self.drcom_logout,
            'grade': self.recentgrade,
            'fullgrade':self.fullgrade,
            #'course':self.course,
            'book_list': self.booklist,
            'drcom_flow': self.drcom,
            #'eggs': self.eggs,
            #'userguide': self.userguide
         }
        lookup.get(key, lambda: None)()
        func = lookup[key]
        return func()
         

