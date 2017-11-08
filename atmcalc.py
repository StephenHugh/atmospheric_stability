# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from math import sin,cos,asin,pi
from pandas import  DataFrame

"""
 calculate the height angle of sun
     mm,dd,hh: month,day,hour(in 24?)
     longitude,latitude: in deg
"""
def sunheightangleCalc(mm,dd,hh,longitude,latitude):
    # calc the sun angle with mm-dd-longitude-latitude, i.e. δ in GB3840-91
    monthday = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    da = sum(monthday[0:mm-1])+dd-1
    theta_0 = 360*da/365*pi/180 # as reg to fit the cos() and sin()
    sunangle = ( 0.006918-0.399912*cos(theta_0)+0.070257*sin(theta_0)- \
            0.006758*cos(2*theta_0)+0.000907*sin(2*theta_0)- \
            0.002697*cos(3*theta_0)+0.001480*sin(3*theta_0) )*180/pi # as deg
    # calc the height angle of sun, i.e. h_0 in GB3840-91
#    print(sunangle)
    sunheightangle = asin(sin(latitude*pi/180)*sin(sunangle*pi/180)+ \
            cos(latitude*pi/180)*cos(sunangle*pi/180)* \
            cos((15*hh+longitude-300)*pi/180))*180/pi  #as deg
    print(sunheightangle)
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
#    print(sunheightangle)    
    if hh<8 or hh>=20  :
        night = True
    else:
        night = False
    sunradlevel = sunradlevelCalc(sunheightangle,cloudall,cloudlow,night)
    atmstablelevel = stablelevelQuery(sunradlevel,windspeed,up)
    return atmstablelevel
    
# test code here
df = pd.read_excel('E:/!WORKSPACE/Python/atmospheric_stability/metadata/tmp2.xlsx')
longitude = 116.3400271259
latitude = 39.7428682551
stablelevelseries = []  # calculated stable level data in series 
windspeedlevelseries = [] # wind speed level data in series
windspeedsection = [] # wind speed sections as string in list
windspeeddivide = [0,1,2,3,5,6] # it can be changed freely
for i in range(len(windspeeddivide)-1):
    windspeedsection.append('%.1f-%.1f'%(windspeeddivide[i],windspeeddivide[i+1]-0.1))
windspeedsection.append('≥%.1f'%(windspeeddivide[-1]))
for i in df.index:
    mm = df['月份'].iat[i]
    dd = df['日期'].iat[i]
    hh = df['时次'].iat[i]
    windspeed = df['定时风速(m/s)'].iat[i]
    if windspeed>=windspeeddivide[-1]:
        windspeedlevelseries.append(windspeedsection[-1])   
    else:
        for j in range(len(windspeeddivide)-1):
            if windspeed>=windspeeddivide[j] and windspeed<windspeeddivide[j+1]:
                windspeedlevelseries.append(windspeedsection[j])
    cloudall = df['定时总云量(成)'].iat[i]
    cloudlow = df['定时低云量(成)'].iat[i]
    stablelevelseries.append(stablelevelCalc(mm,dd,hh,longitude,latitude,windspeed,cloudall,cloudlow,True))
df['大气稳定度等级']=stablelevelseries
df['定时风速']=windspeedlevelseries
# print(stablelevelseries)
df2=df[['大气稳定度等级','定时风速','定时风向']]
grouped=df2.groupby([df2['大气稳定度等级'],df2['定时风速'],df2['定时风向']])
count = grouped.size()
#print(grouped.size())
cross = pd.crosstab([df2['大气稳定度等级'],df2['定时风速']],df2['定时风向'],margins=True)
# shape the frame of results, absolute frequency and frequency

resultframe = DataFrame(np.zeros([6*len(windspeedsection),17]), \
        index=[['A','A','A','A','A','A','B','B','B','B','B','B', \
        'C','C','C','C','C','C','D','D','D','D','D','D', \
        'E','E','E','E','E','E','F','F','F','F','F','F'], \
        windspeedsection*6],columns= \
        ['C','N','NNE','NE','ENE','E','ESE','SE','SSE','S', \
        'SSW','SW','WSW','W','WNW','NW','NNW'])
# get the absolute frequency table
absolutefreq = cross.reindex(index=resultframe.index,columns=resultframe.columns,fill_value=0)
# get the sum of each stability
stablelevelsum = (absolutefreq.sum(level=0)).sum(axis=1)
freq = absolutefreq.copy()
for i in range(len(resultframe.index.levels[0])): 
    if stablelevelsum[i] == 0: 
         freq[i*len(windspeedsection):((i+1)*len(windspeedsection))] = 0
    else:
        freq[i*len(windspeedsection):((i+1)*len(windspeedsection))] = \
            absolutefreq[i*len(windspeedsection):((i+1)*len(windspeedsection))] / \
            stablelevelsum[i]
with pd.ExcelWriter('atmospheric stabilities.xlsx') as writer:
    df.to_excel(writer,sheet_name='Input')
    absolutefreq.to_excel(writer,sheet_name='联合频数')
    freq.to_excel(writer,sheet_name='联合频率')
        

#print(absolutefreq)


# test code end










