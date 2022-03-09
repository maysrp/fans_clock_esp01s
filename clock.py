import time
import ntptime
import network
import urequests
from machine import RTC
import gc
import ujson

class Clock:
    def __init__(self,key=0,city=0,id=0,acfun=0):
        self.c={}
        self.key=key
        self.city=city
        self.acfun=acfun
        self.id=id #你的Bilibil的ID
        self.ntp()
        self.rtc=RTC()
    def net(self):
        self.wlan = network.WLAN(network.STA_IF) 
        self.wlan.active(True)
        self.c["status"]=False
        if self.wlan.isconnected():
            self.c["status"]=True
    def ntp(self):
        ntptime.host="ntp1.aliyun.com"
        ntptime.NTP_DELTA = 3155644800
        try:
            ntptime.settime()
            self.c["status"]=True
            self.c["info"]="NTP is done!"
        except Exception as e:
            self.c["status"]=False
            self.c["info"]="wifi Error"
    def show_time(self):
        date=self.rtc.datetime()
        self.m=date[5]
        self.h=date[4]
        self.hour=str(self.h) if len(str(self.h))==2 else ' '+str(self.h)
        self.min=str(self.m) if len(str(self.m))==2 else '0'+str(self.m)
    def bfans(self):
        url="http://api.bilibili.com/x/relation/stat?vmid="+str(self.id)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE' }
        try:
            re=urequests.get(url,headers=headers)
            my=re.json()
        except Exception as e:
            my={"code":233}
        if my['code']==0:
            self.bfans_count= my['data']['follower']
            self.bfan=self.bfans_count
        else:
            self.bfans_count=False
            self.bfan=False
    def backfans(self):
        if type(self.bfans_count).__name__=='int':
            if self.bfans_count<10000:
                return str(self.fans_count)
            elif self.bfans_count<1000000:
                ka=self.bfans_count//1000
                return str(ka)+'K'
            else:
                ka=self.bfans_count//1000000
                return str(ka)+'M'
        else:
            return 'None'
    def afans(self):
        gc.collect()    
        url="https://www.acfun.cn/rest/pc-direct/user/userInfo?userId="+str(self.acfun)
        headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36' }
        try:
            re=urequests.get(url,headers=headers)
            ca=re.text
            cc=ujson.loads(ca)
        except Exception as e:
            cc={}
            cc['result']=1
        if cc['result']==0:
            self.afan=cc['profile']['followed'].replace('\u4e07','W')
        else:
            self.afan='0'
    def weather(self):
        url="http://api.seniverse.com/v3/weather/now.json?key=%s&location=%s&language=zh-Hans&unit=c" % (self.key,self.city)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE' }
        ba=[]
        try:
        # print(url)
            re=urequests.get(url,headers=headers)
            my=re.json()
            ba.append(my['results'][0]['now']['code'])
            ba.append(my['results'][0]['now']['temperature'])
        except Exception as e:
            return False
        return ba