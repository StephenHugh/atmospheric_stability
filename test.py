# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from math import sin,cos,asin,pi
from pandas import Series, DataFrame

"""
 calculate the height angle of sun
     mm,dd,hh: month,day,hour(in 24?)
     longitude,latitude: in deg
"""
def sunheightangleCalc(mm,dd,hh,longitude,latitude):
    # calc the sun angle with mm-dd-longitude-latitude, i.e. delta in GB3840-91
    monthday = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    da = sum(monthday[0:mm-1])+dd
    theta_0 = 360*da/365*pi/180 # as reg to fit the cos() and sin()
    sunangle = ( 0.006918-0.399912*cos(theta_0)+0.070257*sin(theta_0)- \
            0.006758*cos(2*theta_0)+0.000907*sin(2*theta_0)- \
            0.002697*cos(3*theta_0)+0.001480*sin(3*theta_0) )*180/pi # as deg
    # calc the height angle of sun, i.e. h_0 in GB3840-91
    sunheightangle = asin(sin(latitude*pi/180)*sin(sunangle*pi/180)+ \
            cos(latitude*pi/180)*cos(sunangle*pi/180)* \
            cos((15*hh+longitude-300)*pi/180))*180/pi  #as deg
    return sunheightangle

"""
 calculate the radiation level of sun
"""
def sunradlevelCalc(sunheightangle,cloudall,cloudlow,night):
    h0 = abs(sunheightangle)
    if cloudall<=4 and cloudlow<=4:
        if night:
            rad = -2
        elif h0<=15:
            rad = -1
        elif h0>15 and h0<=35:
            rad = 1
        elif h0>35 and h0<=65:
            rad = 2
        else:
            rad = 3
    elif cloudall>4 and cloudall<8 and cloudlow<=4:
        if night:
            rad = -1
        elif h0<=15:
            rad = 0
        elif h0>15 and h0<=35:
            rad = 1
        elif h0>35 and h0<=65:
            rad = 2
        else:
            rad = 3
    elif cloudall>=8 and cloudlow<=4:
        if night:
            rad = -1
        elif h0<=15:
            rad = 0
        elif h0>15 and h0<=35:
            rad = 0
        elif h0>35 and h0<=65:
            rad = 1
        else:
            rad = 1
    elif cloudall>=5 and cloudlow<8 and cloudlow>4:
        if night:
            rad = 0
        elif h0<=15:
            rad = 0
        elif h0>15 and h0<=35:
            rad = 0
        elif h0>35 and h0<=65:
            rad = 0
        else:
            rad = 1
    elif cloudall>=8 and cloudlow>=8:
        if night:
            rad = 0
        elif h0<=15:
            rad = 0
        elif h0>15 and h0<=35:
            rad = 0
        elif h0>35 and h0<=65:
            rad = 0
        else:
            rad = 0
    else:
        rad = 99
    return rad

"""
 query the stable level of atmosphere from table in GB3840-91
     radlevel: from 3 to -3
     windseed: from 0 to inf
     up: indicate if A-B set as B,B-C as C, C-D as D; default as no up setting
     return value err: X - wrong radlevel input, x - wrong windspeed input
"""
def stablelevelQuery(radlevel,windspeed,up=False):
    if not up:  # set A-B as A        
        if windspeed<2 and windspeed>=0:
            spliter = {
                3:'A',
                2:'A',
                1:'B',
                0:'D',
                -1:'E',
                -2:'F'}
            stablelevel = spliter.get(radlevel,'X')
        elif windspeed<3 and windspeed>=2:
            spliter = {
                3:'A',
                2:'B',
                1:'C',
                0:'D',
                -1:'E',
                -2:'F',}
            stablelevel = spliter.get(radlevel,'X')
        elif windspeed<5 and windspeed>=3:
            spliter = {
                3:'B',
                2:'B',
                1:'C',
                0:'D',
                -1:'D',
                -2:'E',}
            stablelevel = spliter.get(radlevel,'X')
        elif windspeed<6 and windspeed>=5:
            spliter = {
                3:'C',
                2:'C',
                1:'D',
                0:'D',
                -1:'D',
                -2:'D',}
            stablelevel = spliter.get(radlevel,'X')
        elif windspeed>=6:
            spliter = {
                3:'C',
                2:'D',
                1:'D',
                0:'D',
                -1:'D',
                -2:'D',}
            stablelevel = spliter.get(radlevel,'X')
        else:
            stablelevel = 'x'
    else:
        if windspeed<2 and windspeed>=0:
            spliter = {
                3:'A',
                2:'B',
                1:'B',
                0:'D',
                -1:'E',
                -2:'F',}
            stablelevel = spliter.get(radlevel,'X')
        elif windspeed<3 and windspeed>=2:
            spliter = {
                3:'B',
                2:'B',
                1:'C',
                0:'D',
                -1:'E',
                -2:'F',}
            stablelevel = spliter.get(radlevel,'X')
        elif windspeed<5 and windspeed>=3:
            spliter = {
                3:'B',
                2:'C',
                1:'C',
                0:'D',
                -1:'D',
                -2:'E',}
            stablelevel = spliter.get(radlevel,'X')
        elif windspeed<6 and windspeed>=5:
            spliter = {
                3:'C',
                2:'D',
                1:'D',
                0:'D',
                -1:'D',
                -2:'D',}
            stablelevel = spliter.get(radlevel,'X')
        elif windspeed>=6:
            spliter = {
                3:'C',
                2:'D',
                1:'D',
                0:'D',
                -1:'D',
                -2:'D',}
            stablelevel = spliter.get(radlevel,'X')
        else:
            stablelevel = 'x'
    return stablelevel

def stablelevelCalc(mm,dd,hh,longitude,latitude,windspeed,cloudall,cloudlow,up=False):
    sunheightangle = sunheightangleCalc(mm,dd,hh,longitude,latitude) # in deg
    if hh<8 or hh>=20  :
        night = True
    else:
        night = False
    sunradlevel = sunradlevelCalc(sunheightangle,cloudall,cloudlow,night)
    atmstablelevel = stablelevelQuery(sunradlevel,windspeed,up)
    return atmstablelevel
    
# test code here
df = pd.read_excel('E:/!WORKSPACE/Python/atmospheric_stability/metadata/tmp3.xlsx')

mm = 6
dd = 25
hh = 12
longitude=0
latitude = 0
print(sunheightangleCalc(mm,dd,hh,longitude,latitude))

#test code end










