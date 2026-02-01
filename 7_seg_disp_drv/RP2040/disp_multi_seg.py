from machine import Pin, SPI

class DispMultiSeg:

    def __init__(self, baudrate=1_000_000, sck=2, cs=1, mosi=3, miso=0):
        self.digit  = [0, 0, 0, 0, 0, 0]
        self.rd0 = 0
        self.rd1 = 0
        ######################
        # RP2040 SPI setting
        self.SCK  = sck
        self.CS   = cs
        self.MOSI = mosi
        self.MISO = miso
        # Chip Select pin
        self.cs = Pin(self.CS, Pin.OUT, value=1)
        # SPI configuration (MODE 0, MSB first)
        self.spi = SPI(0,
                baudrate = baudrate,
                polarity = 0,
                phase    = 0,
                bits     = 8,
                firstbit = SPI.MSB,
                sck      = Pin(self.SCK),
                mosi     = Pin(self.MOSI),
                miso     = Pin(self.MISO))

    def spi_exchange(self, addr, data):
        Read_buf  = bytearray(2)
        Write_buf = bytearray(2)
        Write_buf[0] = addr
        Write_buf[1] = data
        self.cs.value(0)          # Select FPGA
        self.spi.write_readinto(Write_buf, Read_buf)
        self.cs.value(1)          # Deselect FPGA
        self.rd0 = Read_buf[0]
        self.rd1 = Read_buf[1]

    def set_digit(self, pos, dig):
        self.digit[pos] = dig

    def get_digit(self, pos):
        return self.digit[pos]

    def set_seg(self, pos, seg):
        self.digit[pos] = self.digit[pos] | seg

    def clr_seg(self, pos, seg):
        self.digit[pos] = self.digit[pos] & (~seg)

    def shift_digit(self, dir_right=True, rotate=False):
        if dir == True: # right
          tmp = self.digit[0]
          for i in range(6):
              self.digit[i] = self.digit[i+1]
          self.digit[5] = tmp if rotate else 0
        else: # left
          tmp = self.digit[5]
          for i in range(6):
              self.digit[5-i] = self.digit[5-i-1]
          self.digit[0] = tmp if rotate else 0

    def clr_digit_all(self):
        for m in self.digit:
            m = 0

    def disp_write_digit(self, pos, dig):
        self.set_digit(pos, dig)
        self.disp_update_digit(pos)

    def disp_write_digit_all(self, digits):
        for pos, dig in enumerate(digits):
          self.set_digit(pos, dig)
        self.disp_update_digit_all()

    def disp_update_digit(self, pos):
        self.spi_exchange(pos, self.digit[pos])

    def disp_update_digit_all(self):
        for addr, dig in enumerate(self.digit):
            self.spi_exchange(addr, dig)

    def disp_clear(self):
        self.disp_write_digit_all([0, 0, 0, 0, 0, 0])
