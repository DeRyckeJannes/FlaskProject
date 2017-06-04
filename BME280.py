import smbus
import time

bus = smbus.SMBus(1)
address = 0x77

temperatureCompensationParameters = bus.read_i2c_block_data(address, 0x88, 6)
# compensatie parameters maar 1 keer inlezen data van sensor blijven inlezen
# unsigned integer value stored in two complement
# print(temperatureCompensationParameters)
# temperature
dig_T1 = temperatureCompensationParameters[1] << 8 | temperatureCompensationParameters[0]  # 0x88 & 0x09
dig_T2 = temperatureCompensationParameters[3] << 8 | temperatureCompensationParameters[2]  # 0x88 & 0x09
dig_T3 = temperatureCompensationParameters[5] << 8 | temperatureCompensationParameters[4]  # 0x88 & 0x09
# 2 complement uitrekenen
if dig_T2 > 32767:
    dig_T2 -= 65536
if dig_T3 > 32767:
    dig_T3 -= 65536

# temperatuur inlezen
temperatureXLSB = bus.read_byte_data(address, 0xFC)
temperatureLSB = bus.read_byte_data(address, 0xFB)
temperatureMSB = bus.read_byte_data(address, 0xFA)
temperatureValue = ((temperatureMSB << 16) | (temperatureLSB << 8) | (temperatureXLSB & 0xF0)) >> 4
# print("temperature value: "+str(temperatureValue))

# bereken temperatuur
var1 = (((temperatureValue >> 3) - (dig_T1 << 1)) * (dig_T2) >> 11)
var2 = ((((temperatureValue >> 4) - (dig_T1) * ((temperatureValue >> 4) - (dig_T1) >> 12))) * (dig_T3) >> 14)
# print(var1)
# print(var2)
t_fine = (var1 | var2)
T = (t_fine * 5 + 128) >> 8
print(T)
T = T / 100


# ----------------------------------------------------------------------------------------------------------------------#
dig_H1 = bus.read_byte_data(address, 0xA1)
humidityCompensationParameters = bus.read_i2c_block_data(address, 0xE1, 7)
# Convert the data
# Humidity coefficients
dig_H2 = humidityCompensationParameters[1] << 8 | humidityCompensationParameters[0]
if dig_H2 > 32767:
    dig_H2 -= 65536
dig_H3 = (humidityCompensationParameters[2] & 0xFF)
dig_H4 = (humidityCompensationParameters[3] << 4) | (humidityCompensationParameters[4] & 0xF)
if dig_H4 > 32767:
    dig_H4 -= 65536
dig_H5 = (humidityCompensationParameters[4] >> 4) | (humidityCompensationParameters[5] << 4)
if dig_H5 > 32767:
    dig_H5 -= 65536
dig_H6 = humidityCompensationParameters[6]
if dig_H6 > 127:
    dig_H6 -= 256

# Temperature xLSB, Humidity MSB, Humidity LSB
humidityLSB = bus.read_byte_data(address, 0xFE)
humidityMSB = bus.read_byte_data(address, 0xFD)

# Convert the humidity data
adc_H = humidityMSB << 8 | humidityLSB

# Humidity offset calculations
# var_H = (t_fine - 76800)
# var_H = (((((adc_H << 14) - ((dig_H4) << 20) - ((dig_H5) * var_H)) + (16384)) >> 15) * (((((((var_H * (dig_H6)) >> 10) * (((var_H *(dig_H3)) >> 11) + (32768))) >> 10) + (2097152)) * (dig_H2) + 8192) >> 14))
# var_H = (var_H - (((((var_H >> 15) * (var_H >> 15)) >> 7) * (dig_H1)) >> 4))
# if var_H<0:
#     var_H=0
# else:
#     var_H=var_H
#
# if var_H> 419430400:
#     var_H=419430400
# else:
#     var_H=var_H
#
# var_H=var_H/1024


var_H = ((t_fine) - 76800.0)
var_H = (adc_H - (dig_H4 * 64.0 + dig_H5 / 16384.0 * var_H)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * var_H * (1.0 + dig_H3 / 67108864.0 * var_H)))
humidity = var_H * (1.0 -  dig_H1 * var_H / 524288.0)
if humidity > 100.0 :
    humidity = 100.0
elif humidity < 0.0 :
    humidity = 0.0
print("relative humidity: " + str(var_H))
