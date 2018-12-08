
from machine import Pin
import dht
import time
import taskpro

switch_1 = None
dht11 = None
m = [0, 1]
CloseFlag = -1
def init():
  global switch_1
  global dht11
  switch_1 = Pin(2, Pin.OUT, value = 0)
  dht11 = dht.DHT11(Pin(21))

def switch_chage(i, s):
  if i in [0]:
    switch_1.value(m[s])
    time.sleep(0.5)
    switch_1.value(m[0])

def get_SensorData(n):
  try:
    try:
      dht11.measure()
    except:
      pass
    if n in [0]:
      return (int(dht11.temperature()))
    elif n in [1]:
      return (int(dht11.humidity()))
  except:
    print("An Error occoured in 'get_SensorData")

def get_SwitchData(n):
  if n in [0]:
    return m[int(switch_1.value())]

def set_open():
  global CloseFlag
  door_Handle(True)
  CloseFlag = 8

def door_Handle(status):
  if status:
    Pin(2, Pin.OUT, value = 1)
  else:
    Pin(2, Pin.OUT, value = 0)
  taskpro.Send_SensorData() 

def Door_Control():
  try:
    global CloseFlag
    if CloseFlag == 0:
      door_Handle(False)
      CloseFlag = -1
    else:
      if CloseFlag > 0:
        CloseFlag -= 1
  except:
    pass




