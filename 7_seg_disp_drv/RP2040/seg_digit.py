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

def dig2seg(d):
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

def fmt_dec(value, width=6):
  return f"{value:0{width}d}"

def fmt_dec_seg_array(value):
    dec = fmt_dec(value=value, width=6)
    seg = []
    for i in (dec):
        d = int(i)
        seg.append(dig2seg(d))
    return seg
