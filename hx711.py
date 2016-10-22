import RPi.GPIO as GPIO
import time

class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        self.PD_SCK = pd_sck
        self.DOUT = dout

        GPIO.setmode(GPIO.BCM)  # use Broadcom pin numbers GPIOxx rather than Pi pin header numbers
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0

        GPIO.output(self.PD_SCK, True)
        GPIO.output(self.PD_SCK, False)

        self.set_gain(gain);

    def is_ready(self):
        return GPIO.input(self.DOUT) == 0

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        GPIO.output(self.PD_SCK, False)
        self.read()

    def read(self):
        while not self.is_ready():
            #print("WAITING")
            pass

        dataBits = [];

        for i in range(24):
            GPIO.output(self.PD_SCK, True)
            dataBits.append( GPIO.input(self.DOUT) )
            GPIO.output(self.PD_SCK, False)

        #set channel and gain factor for next reading
        for i in range(self.GAIN):
            GPIO.output(self.PD_SCK, True)
            GPIO.output(self.PD_SCK, False)

        # Pad out to 32 bits 2's complement
        if dataBits[0]:
            for i in range(8):
                dataBits.insert(0, 1)
        else:
            for i in range(8):
                dataBits.insert(0, 0)

        result = 0
        for bit in dataBits:
            result = (result << 1) | bit

        # Two's complement    
        if (result & (1<<31)):
            result = result - (1 << 32)

        return result
        
    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)
        
############# EXAMPLE
hx = HX711(17, 27)
hx.set_scale(1)
#hx.tare()

while True:
    try:
        #val = hx.get_units(3)
        val = hx.read();
        time.sleep(1)
        print val
        #hx.power_down()
        #time.sleep(.001)
        #hx.power_up()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
