
import json
import taskpro
import sensor
import LCD12832

def User_CallBack(c):
  print(c)
  try:
    load_js = json.loads(c)
  except:
    print("JSON解析失败")
    return()
  try:
    function = load_js['msg']
  except:
    function = None
  print(function) 
  
  try:
    if function == "rec":
      taskpro.Send_SensorData()
    elif function == "usr":
      try:
          name = load_js['name']
      except:
          name = " "
      if load_js['sta']:
        sensor.set_open()
        taskpro.Send_SensorData((name)) 
        LCD12832.Display_Message(1, name)
      else:
        LCD12832.Display_Message(2, name)
    elif function == "wel":
      LCD12832.Display_Message(0, " ")
    elif function == "swt":
      try:
        if load_js['dev'] == 0 and load_js['sta'] == 1:
          sensor.set_open()
          LCD12832.Display_Message(1, "   Manual operation")
      except:
        print("开关操作错误")
      taskpro.Send_SensorData()
  except:
    print("消息任务处理错误")








