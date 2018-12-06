
from machine import Pin
import time
import taskpro

switch_1 = None
m = [0, 1]
CloseFlag = -1
def init_switch():
  global switch_1
  switch_1 = Pin(2, Pin.OUT, value = 0)
  
def switch_chage(i, s):

  if i in [0]:
    switch_1.value(m[s])
    time.sleep(0.5)
    switch_1.value(m[0])

def get_SensorData(n):
  if n in [0]:
    return m[int(switch_1.value())]

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


