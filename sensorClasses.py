class sensors():
    def __init__(self):
        import smbus
        import spidev
        self.__bus = smbus.SMBus(1)
        self.__address = 0x77
        self.__spi = spidev.SpiDev()  # create spi object
        self.__spi.open(0, 0)  # open spi port 0, device (CS) 0

    def ReadCompensationParametersTemp(self): #run once compensation parameters are always the same
        temperatureCompensationRegisters = self.__bus.read_i2c_block_data(self.__address, 0x88, 6)
        # compensatie parameters maar 1 keer inlezen data van sensor blijven inlezen
        # unsigned integer value stored in two complement
        # print(temperatureCompensationRegisters)
        # temperature
        dig_T1 = temperatureCompensationRegisters[1] << 8 | temperatureCompensationRegisters[0]  # 0x88 & 0x09
        dig_T2 = temperatureCompensationRegisters[3] << 8 | temperatureCompensationRegisters[2]  # 0x88 & 0x09
        dig_T3 = temperatureCompensationRegisters[5] << 8 | temperatureCompensationRegisters[4]  # 0x88 & 0x09
        # 2 complement uitrekenen
        if dig_T2 > 32767:
            dig_T2 -= 65536
        if dig_T3 > 32767:
            dig_T3 -= 65536
        temperatureCompensationParameters=[dig_T1,dig_T2,dig_T3]
        return temperatureCompensationParameters

    def CalculateTemperature(self, temperatureCompensationParameters):
        temperatureXLSB = self.__bus.read_byte_data(self.__address, 0xFC)
        temperatureLSB = self.__bus.read_byte_data(self.__address, 0xFB)
        temperatureMSB = self.__bus.read_byte_data(self.__address, 0xFA)
        temperatureValue = ((temperatureMSB << 16) | (temperatureLSB << 8) | (temperatureXLSB & 0xF0)) >> 4
        var1 = (((temperatureValue >> 3) - (temperatureCompensationParameters[0] << 1)) * (temperatureCompensationParameters[1]) >> 11)
        var2 = ((((temperatureValue >> 4) - (temperatureCompensationParameters[0]) * ((temperatureValue >> 4) - (temperatureCompensationParameters[0]) >> 12))) * (temperatureCompensationParameters[2]) >> 14)
        t_fine = (var1 | var2)
        T = (t_fine * 5 + 128) >> 8
        T = T / 100
        return t_fine, T

    def ReadCompensationParametersHumidity(self):
        dig_H1 = self.__bus.read_byte_data(self.__address, 0xA1)
        humidityCompensationRegisters = self.__bus.read_i2c_block_data(self.__address, 0xE1, 7)
        dig_H2 = humidityCompensationRegisters[1] << 8 | humidityCompensationRegisters[0]
        if dig_H2 > 32767:
            dig_H2 -= 65536
        dig_H3 = (humidityCompensationRegisters[2] & 0xFF)
        dig_H4 = (humidityCompensationRegisters[3] << 4) | (humidityCompensationRegisters[4] & 0xF)
        if dig_H4 > 32767:
            dig_H4 -= 65536
        dig_H5 = (humidityCompensationRegisters[4] >> 4) | (humidityCompensationRegisters[5] << 4)
        if dig_H5 > 32767:
            dig_H5 -= 65536
        dig_H6 = humidityCompensationRegisters[6]
        if dig_H6 > 127:
            dig_H6 -= 256
        humidityCompensationParameters=[dig_H1,dig_H2,dig_H3,dig_H4,dig_H5,dig_H6]
        return humidityCompensationParameters

    def CalculateHumidity(self,humidityCompensationParameters,t_fine):
        humidityLSB = self.__bus.read_byte_data(self.__address, 0xFE)
        humidityMSB = self.__bus.read_byte_data(self.__address, 0xFD)
        # Convert the humidity data
        adc_H = humidityMSB << 8 | humidityLSB
        var_H = ((t_fine) - 76800.0)
        var_H = (adc_H - (humidityCompensationParameters[3] * 64.0 + humidityCompensationParameters[4] / 16384.0 * var_H)) * (
        humidityCompensationParameters[1] / 65536.0 * (1.0 + humidityCompensationParameters[5] / 67108864.0 * var_H * (1.0 + humidityCompensationParameters[2] / 67108864.0 * var_H)))
        humidity = var_H * (1.0 - humidityCompensationParameters[0] * var_H / 524288.0)
        if humidity > 100.0:
            humidity = 100.0
        elif humidity < 0.0:
            humidity = 0.0
        return humidity

    def __ReadChannel(self,channel):
        adc = self.__spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3 << 8) | adc[2])  # in byte 1 en 2 zit resultaat
        return data
    def ReadWindspeed(self):
        windspeed=self.__ReadChannel(6)
        windspeed=(windspeed/1023)*3.3
        windspeed=windspeed-0.54
        if (windspeed<=0):
            windspeed=0
        windspeed=(((windspeed/1.6)*32)*3.6)
        return windspeed

    def ReadRaindDrop(self): # rain drop sensor can also be connected to 5v and MCP3008 for more values but we just want to know if it is raining or not.
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21,GPIO.IN)
        if GPIO.input(21)==0:
            return("It is Raining!")
        if GPIO.input(21)==1:
            return("It is not Raining!")




# mijnBME=sensors()
# humidityCompensationParameters=mijnBME.ReadCompensationParametersHumidity()
# temperatureCompensationParameters= mijnBME.ReadCompensationParametersTemp()
# t_fine,T=mijnBME.CalculateTemperature(temperatureCompensationParameters)
# print T
# print t_fine
# humidity=mijnBME.CalculateHumidity(humidityCompensationParameters,t_fine)
# print humidity
# raindrop=mijnBME.ReadRaindDrop()
# print raindrop