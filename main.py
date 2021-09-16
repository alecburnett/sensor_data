#!/usr/bin/env python3

import datetime
main_time_stamp = datetime.datetime.now()

import smbus
import pandas as pd
import time

columns = columns = ['temperature_ext','temperature_int','humidity','pressure', 'brightness', 'time_stamp']
blankdf = pd.DataFrame(columns=columns)

#take average from 60 readings - *warms sensors up - internet suggests first readings after period of inactivity innaccurate..
for i in range(60):
    time.sleep(1)   

    #these values are sourced from: https://wiki.52pi.com/index.php/DockerPi_Sensor_Hub_Development_Board_SKU:_EP-0106
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

    #variables for data frame
    temperature_ext = aReceiveBuf[TEMP_REG]
    temperature_int = aReceiveBuf[ON_BOARD_TEMP_REG]
    humidity        = aReceiveBuf[ON_BOARD_HUMIDITY_REG]
    pressure        = aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16
    brightness      = aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]
    if aReceiveBuf[HUMAN_DETECT] == 1 :
        human_present = 'true'
    else:
        human_present = 'false'

    #dataframe
    df = pd.DataFrame(columns = columns)
    df.loc[0] = [temperature_ext, temperature_int, humidity, pressure, brightness, main_time_stamp] 
    blankdf = blankdf.append(df)       


new_df        = pd.DataFrame(columns = ['temperature_ext', 'temperature_ext_v',
                                        'temperature_int', 'temperature_int_v',
                                        'humidity', 'humidity_v',
                                        'pressure', 'pressure_v', 
                                        'brightness', 'brightness_v', 
                                        'time_stamp'])

new_df.loc[0] = [       blankdf["temperature_ext"].mean(), 
                        blankdf["temperature_ext"].max() - blankdf["temperature_ext"].min(),
                        blankdf["temperature_int"].mean(), 
                        blankdf["temperature_int"].max() - blankdf["temperature_int"].min(),
                        blankdf["humidity"].mean(), 
                        blankdf["humidity"].max() - blankdf["humidity"].min(),
                        blankdf["pressure"].mean(), 
                        blankdf["pressure"].max() - blankdf["pressure"].min(),
                        blankdf["brightness"].mean(), 
                        blankdf["brightness"].max() - blankdf["brightness"].min(),
                        main_time_stamp]
print(new_df)

#database
table = 'sensor-hub-data'
from functions import *
append_db(new_df, table, engine)
