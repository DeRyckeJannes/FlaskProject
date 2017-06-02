import spidev
import RPi.GPIO as GPIO
import time
# 0.4V (0 m/s wind) up to 2.0V (for 32.4m/s wind speed).
# You'll have to remember that the ADC has a base of 3.3V and your max voltage output from the anemometer will only be 2 volts...'
# so if 1023 is 3.3v, then 2 volts would be around a 620 reading {(2/3.3) * 1023}





# open SPI bus
spi = spidev.SpiDev()  # create spi object
spi.open(0, 0)  # open spi port 0, device (CS) 0

# function to read SPI data from MCP3008 chip
# channel must be an integer 0-7
def ReadChannel(channel):
    # 3 bytes versturen
    # 1, S D2 D1 D0 xxxx, 0
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3 << 8) | adc[2])  # in byte 1 en 2 zit resultaat
    return data

# hoofdprogramma
print("program is running")
try:
    while True:
        windsnelheid=ReadChannel(6)
        windsnelheid=(windsnelheid/1023)*3.3
        windsnelheid=windsnelheid-0.54
        if (windsnelheid<=0):
            windsnelheid=0
        windsnelheid=(((windsnelheid/1.6)*32)*3.6)
     #   print(windsnelheid)
        raindrop=ReadChannel(5)
        print(raindrop)

except KeyboardInterrupt:
    print("spi afsluiten")
    spi.close()

print("einde")
GPIO.cleanup()