
from machine import Timer, Pin
import sys
import time
#import BreathLight
import sensor
import LCD12832
import WIFI
import Tcp

deviceID = "5S798O3514V1WT0Y"
ptime = 0
TCP_ResetFlag = 0
def AntiDeathloop(): #将P23拉低即可中断程序继续
  ABP = Pin(23, Pin.OUT, value = 1)
  if not ABP.value():
    print("AntiDeathlooped!")
    sys.exit()

def init():
  AntiDeathloop()
  sensor.init()
  try:
    LCD12832.init()
    LCD12832.Display_6x8_string(4, 1, "System initializing")
    init_WIFITimer()
    #Init_wifiConnect()
    print("init Process")
  except:
    pass

def Init_wifiConnect():
  LCD12832.Display_6x8_string(4, 1, "Wifi Connecting....")
  if WIFI.Connect_WiFi_2():
    LCD12832.Display_6x8_string(4, 1, "Wifi Connected     ")
  try:
    Tcp.TCP_Begin()
    init_mainTimer()
    Send_login()
    time.sleep(0.5)
    Send_SensorData()
  except:
    pass

def Send_login():
  Tcp.TCP_Send(deviceID)

def Send_SensorData(*name):
  try:
    if not name == ():
      recentPerson = name[0]
    else:
      recentPerson = ""
    Tcp.TCP_Send("#{},{},{},{}#".format(recentPerson,sensor.get_SwitchData(0),sensor.get_SensorData(0),sensor.get_SensorData(1)))
  except:
    print("An Error occoured in 'Send_SensorData'")
    pass
  
def Timer_list():
  try:
    global ptime
    global TCP_ResetFlag
    ptime += 1
    if ptime%(50/10) == 0:
      Tcp.TCP_Recv()
    if ptime%(1000/10) == 0:

      LCD12832.RefreshTime()
      sensor.Door_Control()
    if ptime%(30000/10) == 0:
      Send_SensorData()
    if ptime%(60000/10) == 0:
      TCP_ResetFlag += 1
      if TCP_ResetFlag >= 15:
        Tcp.TCP_Reset()
      ptime = 0
  except:
    print("An Error occoured in 'Timer_list()'")
    pass

def init_mainTimer():
  tim1 = Timer(2)
  tim1.init(period=10, mode=Timer.PERIODIC, callback=lambda t: Timer_list()) 
  
def init_WIFITimer():
  tim4 = Timer(4)
  tim4.init(period=2600, mode=Timer.ONE_SHOT, callback=lambda t: Init_wifiConnect())


