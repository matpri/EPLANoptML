# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:54:21 2020

@author: MPrina
"""
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas
import subprocess
from collections import OrderedDict
import os.path
import time
import pandas as pd
#from libfun import load_json
# from constants import HOURS_IN_LEAP_YEAR

def is_float_try(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def read_indicators(FileName):
    raw_file = open(FileName)
    # raw_file=open(self.resultsfile)
    complete =raw_file.read()
    list_file= complete.split("\n")
    lista=[]
    for a in range(len(list_file)):
        # row=[]
        list_file2= list_file[a].split("\t")
        lista.append([x.strip() for x in list_file2 if x])
    # print(lista[16:26])
    
    indicators=lista[16:69]
    dic={}
    for a in range(len(indicators)):
        if len(indicators[a])>2:
            if is_float_try(indicators[a][1]):
                key=indicators[a][0]
                obj=float(indicators[a][1])
                if key!='' and obj!='':
                    dic[key]=obj
    return dic

def read_costs_tech(FileName):
    raw_file = open(FileName)
    # raw_file=open(self.resultsfile)
    complete =raw_file.read()
    list_file= complete.split("\n")
    lista=[]
    for a in range(len(list_file)):
        # row=[]
        list_file2= list_file[a].split("\t")
        lista.append([x.strip() for x in list_file2 if x])
    # print(lista[16:26])
     
    #costs of the technologies
    dic2={}
    list_var=['Solar thermal', 'Small CHP units', 'Heat Pump gr. 2', 'Heat Storage CHP', 
              'Large CHP units', 'Heat Pump gr. 3', 'Heat Storage Solar', 'Boilers gr. 2 and 3',
              'Large Power Plants', 'Wind', 'Wind offshore', 'Photo Voltaic', 'Wave power',
              'River of hydro', 'Hydro Power', 'Hydro Storage', 'Hydro Pump', 'Nuclear',
              'Geothermal Electr.', 'Electrolyser', 'Hydrogen Storage', 'Charge el1 storage', 
              'Discharge el1 storage', 'El1 storage cap', 'Indv. boilers', 'Indv. CHP', 
              'Indv. Heat Pump', 'Indv. Electric heat','Indv. Solar thermal', 'BioGas Upgrade' ,'Gasification Upgrade',
              'DHP Boiler group 1', 'Waste CHP', 'Absorp. HP (Waste)', 'Biogas Plant', 
              'Gasification Plant', 'BioDiesel Plant', 'BioPetrol Plant', 'BioJPPlant', 
              'Tidal Power', 'CSP Solar Power', 'Carbon Recycling', 'Methanation' ,'Liquidation + JP',
              'Desalination Plant', 'Water storage', 'Gas Storage', 'Oil Storage' ,'Methanol Storage',
              'Interconnection', 'Geothermal Heat', 'Indust. Excess Heat', 'Indust. CHP Electr.',
              'Indust. CHP Heat', 'Electr Boiler Gr 2+3', 'Bicycles' ,'Motorbikes', 'Electric Cars',
              'Conventional Cars', 'DME Buses', 'Diesel Buses', 'DME Trucks', 'Diesel Trucks', 
              'El1 storage cap']
    costs_tech=lista[7:73]
    # print( costs_tech)
    list_found=[]
    for a in range(len(costs_tech)):
        for b in range(len(list_var)):
            if list_var[b] in costs_tech[a] and list_var[b] not in list_found:
                indexList=costs_tech[a].index(list_var[b])
                key2=costs_tech[a][indexList]
                dic_temp={}
                value1=float(costs_tech[a][indexList+1])
                value2=float(costs_tech[a][indexList+2])
                value3=float(costs_tech[a][indexList+3])
                dic_temp['Total Inv. Costs']=value1
                dic_temp['Annual Inv. Costs']=value2
                dic_temp['Fixed O&M']=value3
                dic2[key2]=dic_temp
                list_found.append(list_var[b])
            elif list_var[b] in costs_tech[a] and list_var[b] in list_found:
                indexList=costs_tech[a].index(list_var[b])
                key2=costs_tech[a][indexList]+' doublekey'
                dic_temp={}
                value1=float(costs_tech[a][indexList+1])
                value2=float(costs_tech[a][indexList+2])
                value3=float(costs_tech[a][indexList+3])
                dic_temp['Total Inv. Costs']=value1
                dic_temp['Annual Inv. Costs']=value2
                dic_temp['Fixed O&M']=value3
                dic2[key2]=dic_temp
                list_found.append(key2)
                    
    return dic2


def read_TWh(FileName):
    raw_file = open(FileName)
    # raw_file=open(self.resultsfile)
    complete =raw_file.read()
    list_file= complete.split("\n")
    lista=[]
    for a in range(len(list_file)):
        # row=[]
        list_file2= list_file[a].split("\t")
        lista.append([x.strip() for x in list_file2 if x])
    # print(lista[16:26])
     
    #costs of the technologies
    dic3={}
    TWh=lista[80:86]
    # print(TWh)
    list_found=[]
    # list_keys=[]
    # list_values=[]
    for a in range(len(TWh[0])):
        if is_float_try(TWh[4][a]):
            if TWh[1][a]=='':
                if TWh[0][a]+''+TWh[1][a] not in list_found:
                    dic3[TWh[0][a]+''+TWh[1][a]]=float(TWh[4][a])
                    list_found.append(TWh[0][a]+''+TWh[1][a])
                else:
                    dic3[TWh[0][a]+''+TWh[1][a]+' doublekey']=float(TWh[4][a])
                    list_found.append(TWh[0][a]+''+TWh[1][a]+' doublekey')
            else:
                if TWh[0][a]+' '+TWh[1][a] not in list_found:
                    dic3[TWh[0][a]+' '+TWh[1][a]]=float(TWh[4][a])
                    list_found.append(TWh[0][a]+' '+TWh[1][a])
                else:
                    dic3[TWh[0][a]+' '+TWh[1][a]+' doublekey']=float(TWh[4][a])
                    list_found.append(TWh[0][a]+' '+TWh[1][a]+' doublekey')                    
            # list_keys.append(TWh[0][a]+' '+TWh[1][a])
            # list_values.append(TWh[4][a])

    return dic3

# dic=read_indicators('out_new.txt')#'out_new.txt'
# print(dic)

# dic2=read_costs_tech('out_new.txt')#'out_new.txt'
# print(dic2)

dic3=read_TWh('out_new.txt')#'out_new.txt'
print(dic3)