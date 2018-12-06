from machine import Pin
import codetab
import time
import NTP

LCD_RS = 12
LCD_RES = 14
LCD_CS = 27
LCD_SDA = 26
LCD_SCL = 25
LCD_BGLED = 13
ClearFlag = -1

def GPIO_init():
  Pin(LCD_RS, Pin.OUT, value = 1)
  Pin(LCD_RES, Pin.OUT, value = 1)
  Pin(LCD_CS, Pin.OUT, value = 1)
  Pin(LCD_SDA, Pin.OUT, value = 1)
  Pin(LCD_SCL, Pin.OUT, value = 1)
  Pin(LCD_BGLED, Pin.OUT, value = 0)
  LCD_clear()

def GPIO_H(pin):
  Pin(pin).value(1)

def GPIO_L(pin):
  Pin(pin).value(0)

def LCD_cmd(data):
    GPIO_L(LCD_CS)
    GPIO_L(LCD_RS)
    for i in range (8):
        GPIO_L(LCD_SCL)
        if data & 0x80:
            GPIO_H(LCD_SDA)
        else:
            GPIO_L(LCD_SDA)
        GPIO_H(LCD_SCL)
        data <<= 1
        
def LCD_data(data):
    GPIO_L(LCD_CS)
    GPIO_H(LCD_RS)
    for i in range (8):
        GPIO_L(LCD_SCL)
        if data & 0x80:
            GPIO_H(LCD_SDA)
        else:
            GPIO_L(LCD_SDA)
        GPIO_H(LCD_SCL)
        data <<= 1

def LCD_setAddr(page, column):
    LCD_cmd(0xb0 + page - 1)
    LCD_cmd(0x10 +((column >> 4) & 0x0f))
    LCD_cmd(column & 0x0f)

def LCD_init():
    GPIO_init()
    GPIO_L(LCD_CS)
    GPIO_L(LCD_RES)
    GPIO_H(LCD_RES)
    GPIO_L(LCD_BGLED)
    for i in [0xe2, 0x2c, 0x2e, 0x2f,0x22, 0x81,
              0x1b, 0xa2, 0xc8, 0xa0, 0x40, 0xa6,]:   
        LCD_cmd(i)
    LCD_cmd(0xaf) #Enable Display
    GPIO_H(LCD_CS)

def LCD_clear():
    for i in range (4):
        GPIO_L(LCD_CS)
        LCD_cmd(0xb0+i)
        LCD_cmd(0x10)
        LCD_cmd(0x00)
        for j in range (132):
            LCD_data(0x00)
  
def Display_16x32(page, column, dp):
    GPIO_L(LCD_CS)
    for j in range(2):
        LCD_setAddr(page, column * 32)
        for i in range(32):
            LCD_data(dp[j*32+i])
        page += 1
    GPIO_H(LCD_CS)
    
def Display_16x16(page, column, dp):
    GPIO_L(LCD_CS)
    for j in range(2):
        LCD_setAddr(page, column * 16)
        for i in range(16):
            LCD_data(dp[j*16+i])
        page += 1
    GPIO_H(LCD_CS)
  
def Display_8x16(page, column, dp):
    GPIO_L(LCD_CS)
    for j in range(2):
        LCD_setAddr(page, column * 8)
        for i in range(8):
            LCD_data(dp[j*8+i])
        page += 1
    GPIO_H(LCD_CS)  
    
def Display_6x8(page, column, dp):
    GPIO_L(LCD_CS)
    LCD_setAddr(page, column * 6)
    for i in range(6):
        LCD_data(dp[i])
    GPIO_H(LCD_CS)
    
def Display_6x8_string(page, cloumn, str):
    for i in str:
        code = ord(i) - 32
        try:
            Display_6x8(page, cloumn, codetab.F6x8[code])
        except BaseException:
            pass
        cloumn += 1

def Display_8x16_string(page, cloumn, str):
    for i in str:
        code = ord(i) - 32
        try:
            Display_8x16(page, cloumn, codetab.F8x16[code])
        except BaseException:
            pass
        cloumn += 1


def Display_Message(type, info):
    LCD_init()
    LCD_clear()
    GPIO_H(LCD_BGLED) #背光灯
    if type == 1:
        Display_16x32(1, 0, codetab.f16x32[1])
        Display_16x32(1, 1, codetab.f16x32[2])
        Display_16x32(1, 2, codetab.f16x32[3])
        Display_16x32(1, 3, codetab.f16x32[4])
        Display_6x8_string(3, 1, info)
    elif type == 2:
        Display_8x16_string(1, 1, "ACCESS DENIED!")
        Display_6x8_string(3, 1, info)
    SetClearTime(5)

def ShowMainDisplay():
    LCD_init()
    LCD_clear()
    time.sleep(0.2)
    Display_6x8_string(2, 1, "309 Security System")

def init():
    LCD_init()
    ShowMainDisplay()


def SetClearTime(sec):
    global ClearFlag
    ClearFlag = sec
 
def RefreshTime():
    try:
      global ClearFlag
      if ClearFlag == 0:
        ShowMainDisplay()
        ClearFlag = -1
      else:
        if ClearFlag > 0:
          ClearFlag -= 1
      (year, month, mday, hour, minute, second, weekday, yearday) = NTP.nowNTPtime()
      Display_6x8_string(4, 1, "{:0>4d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}".format(year, month, mday, hour, minute, second)) 
    except:
      print("An Error occoured in 'RefreshTime'")
      pass
 
#if __name__ == '__main__':
#    init()
#    Display_Message(2, " ")
#    time.sleep(2)
#    Display_Message(1, "UserName")
#    time.sleep(2)






