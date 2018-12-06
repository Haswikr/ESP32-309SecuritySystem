import ntptime
import utime
import machine
IF_NTP=0
count=0
def ntpsettime(IF_NTP):
    try:
      ntptime.time()
      ntptime.settime()
      rtc=machine.RTC()
      tampon1=utime.time()
      tampon2=tampon1+8*60*60
      rtc.datetime ( utime.localtime(tampon2)[0:3] + (0,) + utime.localtime(tampon2)[3:6] + (0,))
      IF_NTP=1
      return IF_NTP
    except:
      print('无法从NTP服务器获取时间')
      IF_NTP=0
      return IF_NTP


def nowNTPtime():
    global count
    global IF_NTP
    if ((count%(60*30)==0) or (count%10==0 and IF_NTP==0)): #每30分钟与NTP服务器同步一次，当无法获取NTP时10秒后会重试
        IF_NTP=ntpsettime(IF_NTP)
        utime.sleep(0.1)
        count=0
    count=count+1
    time=utime.localtime() # (year, month, mday, hour, minute, second, weekday, yearday)
    #(year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
    #print (year,'-','%02d' % month, '-','%02d'% mday, ' ', '%2d'% hour, ':', '%02d'% minute, ':','%02d'% second, '  Week:',weekday+1, sep = '')
    return(time)



