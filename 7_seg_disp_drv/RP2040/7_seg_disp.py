from machine import Pin
import time
import shrike
from machine import Pin, SPI

#dot_mem = [[0] * 6 for i in range(6)]
disp_mem = [0, 0, 0, 0, 0, 0]

S_A   = 1 << 0
S_B   = 1 << 1
S_C   = 1 << 2
S_D   = 1 << 3
S_E   = 1 << 4
S_F   = 1 << 5
S_G   = 1 << 6
S_DP  = 1 << 7

DIG_0 = S_A | S_B | S_C | S_D | S_E | S_F
DIG_1 = S_B | S_C
DIG_2 = S_A | S_B | S_G | S_E | S_D
DIG_3 = S_A | S_B | S_G | S_C | S_D
DIG_4 = S_F | S_G | S_B | S_C
DIG_5 = S_A | S_F | S_G | S_C | S_D
DIG_6 = S_A | S_G | S_C | S_D | S_E | S_F
DIG_7 = S_A | S_B | S_C
DIG_8 = S_A | S_B | S_C | S_D | S_E | S_F | S_G
DIG_9 = S_A | S_B | S_C | S_D | S_F | S_G

def dot2dig_mem(x,y):
    dig_x = x/2
    xm = x % 2
    if (y == 0):
        seg = S_A
    elif (y == 1):
        seg = S_F if xm == 0 else S_B
    elif (y == 2):
        seg = S_G
    elif (y == 3):
        seg = S_E if xm == 0 else S_C
    elif (y == 4):
        seg = S_D
    elif (y == 5):
        seg = S_DP
    return dig_x, seg

def dig2char(d):
    if (d == 0):
        return DIG_0
    elif (d == 1):
        return DIG_1
    elif (d == 2):
        return DIG_2
    elif (d == 3):
        return DIG_3
    elif (d == 4):
        return DIG_4
    elif (d == 5):
        return DIG_5
    elif (d == 6):
        return DIG_6
    elif (d == 7):
        return DIG_7
    elif (d == 8):
        return DIG_8
    elif (d == 9):
        return DIG_9
    else:
        return 0

######################
# FPGA initialize
shrike.reset()
shrike.flash("FPGA_bitstream_MCU.bin") 

######################
# Reset
#reset_pin = Pin(14, Pin.OUT, value=1)
#reset_pin.value(0)
#time.sleep(1)
#reset_pin.value(1)
#time.sleep(1)

######################
# RP2040 SPI setting
SCK  = 2  
CS   = 1  
MOSI = 3  
MISO = 0  

# Chip Select pin
cs = Pin(CS, Pin.OUT, value=1)

# SPI configuration (MODE 0, MSB first)
spi = SPI(0,
          baudrate=1_000_000,
          polarity=0,
          phase=0,
          bits=8,
          firstbit=SPI.MSB,
          sck=Pin(SCK),
          mosi=Pin(MOSI),
          miso=Pin(MISO))

def spi_exchange(addr, data):
    Read_buf  = bytearray(2)
    Write_buf = bytearray(2)
    Write_buf[0] = addr
    Write_buf[1] = data
    cs.value(0)          # Select FPGA
    spi.write_readinto(Write_buf, Read_buf)
    cs.value(1)          # Deselect FPGA
    return Read_buf[0], Read_buf[1] #rx[0]

def disp_mem_clr():
    for i in range(6):
        disp_mem[i] = 0

def disp_update():
    for i in range(6):
        spi_exchange(i, disp_mem[i])

# cnt = 0
# while True:
#     time.sleep(0.3)
#     resp0, resp1 = spi_exchange(cnt, 1 << cnt)
#     print(str(resp0))
#     print(str(resp1))
#     cnt += 1
#     if cnt == 6:
#         cnt = 0

disp_interval = 0.5

def disp_one_dig(pos, dig):
    disp_mem_clr()
    disp_mem[pos] = dig
    disp_update()
    time.sleep(disp_interval)

disp_mem[0] = DIG_3 | S_DP
disp_mem[1] = DIG_1
disp_mem[2] = DIG_4
disp_mem[3] = DIG_1
disp_mem[4] = DIG_5
disp_mem[5] = DIG_9

disp_interval = 0.3
disp_update()
time.sleep(1)
for i in range(6):
    for j in range(5):
        disp_mem[5-j] = disp_mem[4-j]
        # disp_mem[j] = disp_mem[j+1]
    disp_mem[0] = 0
    # disp_mem[5] = 0
    disp_update()
    time.sleep(disp_interval)

# disp_interval = 0.2
# for i in range(6):
#     for j in range(10):
#         disp_mem[5-i] = dig2char(j)
#         time.sleep(disp_interval)

disp_interval = 0.1

while True:
    for i in range(6):
        disp_one_dig(i, S_A)
    disp_one_dig(5, S_B)
    for i in range(6):
        disp_one_dig(5-i, S_G)
    disp_one_dig(0, S_E)
    for i in range(6):
        disp_one_dig(i, S_D)
    disp_one_dig(5, S_C)
    for i in range(6):
        disp_one_dig(5-i, S_G)
    disp_one_dig(0, S_F)
