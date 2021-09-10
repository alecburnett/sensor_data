#!/usr/bin/env python3

import smbus
import datetime
import pandas as pd


#these values source from: https://wiki.52pi.com/index.php/DockerPi_Sensor_Hub_Development_Board_SKU:_EP-0106

DEVICE_BUS = 1
DEVICE_ADDR = 0x17
TEMP_REG = 0x01
LIGHT_REG_L = 0x02
LIGHT_REG_H = 0x03
STATUS_REG = 0x04 #off temp
ON_BOARD_TEMP_REG = 0x05
ON_BOARD_HUMIDITY_REG = 0x06
ON_BOARD_SENSOR_ERROR = 0x07
BMP280_TEMP_REG = 0x08
BMP280_PRESSURE_REG_L = 0x09
BMP280_PRESSURE_REG_M = 0x0A
BMP280_PRESSURE_REG_H = 0x0B
BMP280_STATUS = 0x0C
HUMAN_DETECT = 0x0D

bus = smbus.SMBus(DEVICE_BUS)

aReceiveBuf = []

aReceiveBuf.append(0x00)

for i in range(TEMP_REG,HUMAN_DETECT + 1):
    aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

temperature    = aReceiveBuf[TEMP_REG]

humidity       = aReceiveBuf[ON_BOARD_HUMIDITY_REG]

pressure       = aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16

brightness     = aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]

if aReceiveBuf[HUMAN_DETECT] == 1 :
    human_present = 'true'
else:
    human_present = 'false'



time_stamp = datetime.datetime.now()


df = pd.DataFrame(columns = ['temperature','humidity','pressure', 'brightness', 'time_stamp'])

df.loc[0] = [temperature, humidity, pressure, brightness, time_stamp] 

table = 'sensor-hub'


from functions import *
replace_db(df, table, engine)