from machine import I2C, Pin,RTC,WDT,reset,Timer
from ssd1306 import SSD1306_I2C
from font import Font
import gc
import network,time

import ujson

web=False
try:
    f=open("config.ini","r")
    c=f.read()
    cc=ujson.loads(c)
    f.close()
except Exception as e:
    web=True

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
i2c = I2C(scl=Pin(0), sda=Pin(2))
display= SSD1306_I2C(128, 32, i2c)
f=Font(display)
f.text("LOADING...",0,0,16)
f.show()
time.sleep(1)
f.fill()
f.text("w:"+cc['wifi'],0,0,8)
f.text("p:"+cc['password'],0,8,8)
f.text("city:"+cc['city'],0,16,8)
f.text("bili:"+cc['bilibili'],0,24,8)
wlan.connect(cc['wifi'], cc['password'])
f.show()
time.sleep(3)
if not wlan.isconnected():
    wlan.connect(cc['wifi'], cc['password'])
    time.sleep(3)

if not wlan.isconnected():
    f.fill()
    f.text("Connect mpy WIFI",0,0,16)
    f.text("open 192.168.4.1",0,16,12)
    f.show()
    gc.collect()
    web=True

def res(q):
    print("SYSTEM reboot ")
    reset()

if web:
    w=Timer(8)
    w.init(period=300000, mode=Timer.ONE_SHOT, callback=res)
    import web
    web.ha=["wifi","password","api","bilibili","city"]
    web.loop.run_forever() #若没有改文件就启动配网程序
    
    
f.fill()
f.text("HELLO WORLD",0,0,16)
time.sleep(1)
gc.collect()    


from clock import Clock
c=Clock(cc['api'],cc['city'],cc['bilibili'])
c.ntp()
f.fill()
e=c.weather()
j=1
c.bfans()
wdt = WDT()



def weather(a):
    e=c.weather()
    wdt.feed()
    c.ntp()
    if not c.c["status"]:
        f.fill()
        f.text("WIFI ERROR!",0,0,16)
        f.text("Please reboot!",0,15,16)
        f.show()

def bfans(a):
    c.bfans()
    wdt.feed()


t_w=Timer(9)
t_f=Timer(10)
t_w.init(period=3600000, mode=Timer.PERIODIC, callback=weather)#更新天气 60min
t_f.init(period=360000, mode=Timer.PERIODIC, callback=bfans)#更新粉丝 6min

while 1:
    f.fill()
    j=j+1
    if e:
        t=str(e[1])
        f.text(t,88,15,16)
        display.text(".",88+8*len(t),10,1)
        f.text("C",92+8*len(t),15,16)
    c.show_time()
    f.text(c.hour+":"+c.min,0,0,32)
    f.show()
    time.sleep(0.5)
    f.text(c.hour+" "+c.min,0,0,32)
    f.show()
    time.sleep(0.5)
    wdt.feed()
    if j%20==0:
        if c.bfan:
            f.fill()
            f.text("B:"+str(c.bfan),0,0,32)
            f.show()
            time.sleep(1)
            wdt.feed()
    if j==3000:
        j=0
    gc.collect()
