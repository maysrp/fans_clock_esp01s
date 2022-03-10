from machine import I2C, Pin,RTC,WDT,reset
from ssd1306 import SSD1306_I2C
from font import Font
import gc
import network,time

import ujson

try:
    f=open("config.ini","r")
    c=f.read()
    cc=ujson.loads(c)
    f.close()
except Exception as e:
    import web
    web.ha=["wifi","password","api","bilibili","city"]
    web.loop.run_forever() #若没有改文件就启动配网程序

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
i2c = I2C(scl=Pin(0), sda=Pin(2))
display= SSD1306_I2C(128, 32, i2c)
f=Font(display)
f.text("LOADING...",0,0,16)
f.show()
time.sleep(1)
f.fill()
f.text("w:"+cc['wifi'],0,0,16)
f.text("p:"+cc['password'],0,16,16)
wlan.connect(cc['wifi'], cc['password'])
f.show()
time.sleep(3)

if not wlan.isconnected():
    f.fill()
    f.text("Connect mpy WIFI",0,0,16)
    f.text("open 192.168.4.1",0,16,12)
    f.show()
    gc.collect()
    try:
        import web
    except Exception as e:
        pass
    finally:
        web.ha=["wifi","password","api","bilibili","city"]
        web.loop.run_forever() #没有联网就启动配网程序
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
    if j%100==0:
        c.ntp()
        wdt.feed()
        c.bfans()
        wdt.feed()
    if j==3000:
        e=c.weather()
        wdt.feed()
        j=0
        if not c.c["status"]:
            f.fill()
            f.text("WIFI ERROR!",0,0,16)
        f.text("Please reboot!",0,15,16)
        f.show()
    wdt.feed()
    gc.collect()
