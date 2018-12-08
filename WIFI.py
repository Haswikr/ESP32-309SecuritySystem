

#Configure the WIFI function
OutputConfig = None
WIFIconnecting = None
def Connect_WiFi_2():
    import os
    import json
    import network
    import time
    global OutputConfig
    global WIFIconnecting
    WIFIconnecting = 1
    TimeOut = 0
    wifi = network.WLAN(network.STA_IF)  
    wifi.active(False)
    try:
        with open('wifi_config.json','r') as f:
            config = json.loads(f.read())
    # 若初次运行,则将进入excpet,执行配置文件的创建        
    except:
        essid = input('wifi name:') # 输入essid
        password = input('wifi passwrod:') # 输入password
        config = dict(essid=essid, password=password) # 创建字典
        with open('wifi_config.json','w') as f:
            f.write(json.dumps(config)) # 将字典序列化为json字符串,存入wifi_config.json

    #以下为正常的WIFI连接流程        
    if not wifi.isconnected(): 
        print('connecting to network...')
        try:
          wifi.active(True) 
          wifi.connect(config['essid'], config['password']) 
        except:
          pass
        while not wifi.isconnected():
            TimeOut += 1
            time.sleep(0.01)
            if TimeOut >= 1024:
              print('Connect Timeout...Please Check your SSID and Password!')
              os.remove("wifi_config.json")
              return(0)
              break
            pass 
    try:
      OutputConfig = wifi.ifconfig()
      print('network config:', OutputConfig)
    except:
      pass
    WIFIconnecting = 0
    f.close()
    return(1)

def get_ip(i):
  try:
    return str(OutputConfig[i])
  except:
    return "0.0.0.0"




