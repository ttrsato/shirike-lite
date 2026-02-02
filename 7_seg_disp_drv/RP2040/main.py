import time
import random
import shrike
from disp_multi_seg import DispMultiSeg
import seg_digit as sd

######################
# Global variables

DISP_WAIT = 0.1
dm = DispMultiSeg()


######################
# FPGA initialize

shrike.reset()
shrike.flash("FPGA_bitstream_MCU.bin") 


######################
# Function

def pos_dig(x, y):
  dig = int(x/3)
  if (y == 0):
    seg = sd.S_A
  elif (y == 1):
    seg = sd.S_B if x%3 else sd.S_F
  elif (y == 2):
    seg = sd.S_G
  elif (y == 3):
    seg = sd.S_C if x%3 else sd.S_E
  elif (y == 4):
    seg = sd.S_D
  return dig, seg


######################
# Main loop

while True:

  dm.disp_write_digit_all([0, 0, 0, 0, 0, 0])

  for i in range(6):
    d, s = pos_dig(x=i*3+1, y=2)
    dm.set_seg(pos=d, seg=s)
    dm.disp_update_digit_all()
    time.sleep(DISP_WAIT)
    dm.set_digit(d, 0)

  for i in range(6):
    d, s = pos_dig(x=(5-i)*3+1, y=2)
    dm.set_seg(pos=d, seg=s)
    dm.disp_update_digit_all()
    time.sleep(DISP_WAIT)
    dm.set_digit(d, 0)

  dm.set_digit(5, 0)
  d, s = pos_dig(x=0, y=1)
  dm.set_seg(pos=d, seg=s)
  d, s = pos_dig(x=0, y=3)
  dm.set_seg(pos=d, seg=s)
  dm.disp_update_digit_all()
  time.sleep(DISP_WAIT)

  for i in range(6):
    d, s = pos_dig(x=i*3+1, y=0)
    dm.set_seg(pos=d, seg=s)
    d, s = pos_dig(x=i*3+1, y=4)
    dm.set_seg(pos=d, seg=s)
    dm.disp_update_digit_all()
    time.sleep(DISP_WAIT)
    dm.set_digit(d, 0)

  dm.set_digit(5, 0)
  d, s = pos_dig(x=(5+1)*3-1, y=1)
  dm.set_seg(pos=d, seg=s)
  d, s = pos_dig(x=(5+1)*3-1, y=3)
  dm.set_seg(pos=d, seg=s)
  dm.disp_update_digit_all()
  time.sleep(DISP_WAIT)

  for i in range(6):
    d, s = pos_dig(x=(5-i)*3+1, y=2)
    dm.set_seg(pos=d, seg=s)
    dm.disp_update_digit_all()
    time.sleep(DISP_WAIT)
    dm.set_digit(d, 0)

  dm.set_digit(0, 0)
  d, s = pos_dig(x=0, y=1)
  dm.set_seg(pos=d, seg=s)
  dm.disp_update_digit_all()
  time.sleep(DISP_WAIT)

  for j in range(6):
    for i in range(7):
      dm.set_seg(pos=j, seg=1<<(i%6))
      dm.disp_update_digit_all()
      time.sleep(DISP_WAIT)
      dm.set_digit(j, 0)

  for i in range(6):
    dm.set_seg(pos=5-i, seg=sd.S_DP)
    dm.disp_update_digit_all()
    time.sleep(DISP_WAIT)
    dm.set_digit(5-i, 0)

  pi = [9, 5, 1, 4, 1, 3]

  for p, d in enumerate(pi):
    c = sd.dig2seg(d)
    for i in range(6-p):
      dm.set_digit(i, c)
      if d == 3:
        dm.set_seg(0, sd.S_DP)
      dm.disp_update_digit_all()
      time.sleep(DISP_WAIT)
      dm.set_digit(i, 0)
    dm.set_digit(5-p, c)
    if d == 3:
      dm.set_seg(0, sd.S_DP)
    time.sleep(0.5)

  for i in range(6):
    dm.shift_digit()
    dm.disp_update_digit_all()
    time.sleep(0.5)

  time.sleep(1)

  for i in range(6):
    dm.set_digit(pos=5-i, dig=0xff)
    dm.disp_update_digit_all()
    time.sleep(DISP_WAIT/2.0)

  for i in range(3):
    dm.disp_write_digit_all([0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
    time.sleep(1)
    dm.disp_clear()
    time.sleep(1)

  dm.disp_write_digit_all([0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
  time.sleep(2)

  for i in range(50):
    p = random.randint(0, 5)
    d = random.randint(0, 7)
    dm.clr_seg(pos=p, seg=1<<d)
    dm.disp_update_digit_all()
    time.sleep(0.5)

  for i in range(6):
    dm.set_digit(pos=i, dig=0)
    dm.disp_update_digit_all()
    time.sleep(DISP_WAIT)

