# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 16:30:37 2015

@author: MPrina
Genetic Algorith implemented with deap algorith

version 1.1 to install from master branch of github repository
pip install -U git+http://github.com/DEAP/deap
"""
# from GA import GA
from GAnew import GA
from libeplan import *
from termcolor import colored
import time
from En_Eff_and_HP import func_EF_costs, En_Eff
import pandas as pd

global VARIABLES, START, X, MOLT_FACTORS, INPUTFILE
global ENERGYPLAN, OUT_FOLDER, FUNCTION_2_EVAL
global CONSTRAIN

t0 = time.time()

year=2050#2050#2019
country='IT'

#Input_costs.xlsx
ex_hist = pd.ExcelFile('Input_costs.xlsx')
dfcosts = ex_hist.parse("Sheet1")
# dfPUN = ex_hist.parse("PUN")

# dfPUN=dfPUN.set_index('EPLAN label')
# print(dfcosts)
VarCosts=tuple(dfcosts['EPLAN label'].tolist())
varEP_Costs=dfcosts[year].tolist()

# list_index=list(dfPUN.index)
# for a in range(len(list_index)):
#     VarCosts=VarCosts+(list_index[a], )
#     varEP_Costs.append(dfPUN.loc[list_index[a], country])
# print(VarCosts, varEP_Costs)

def Indust_new(Perc_Ind_eff, data, perc_el_ind, perc_green_gas):
    
    Coal_indu= data['input_fuel_CSHP[1]']*(1-Perc_Ind_eff/100.)
    Oil_indu=data['input_fuel_CSHP[2]']*(1-Perc_Ind_eff/100.)
    Ngas_indu=data['input_fuel_CSHP[3]']*(1-Perc_Ind_eff/100.)
    Bio_indu=data['input_fuel_CSHP[4]']*(1-Perc_Ind_eff/100.)
    
#    print(Ngas_indu)
    el_dem_indu=Ngas_indu*perc_el_ind/100.
    Ngas_indu_result_el=Ngas_indu-Ngas_indu*perc_el_ind/100.#natural gas that still remains after electrification
    el_demand=data['Input_el_demand_Twh']+el_dem_indu
    Ngas_indu_result_gg=Ngas_indu*perc_green_gas/100.#gg stands for green gas
    
    Ngas_indu_tot=Ngas_indu_result_el-Ngas_indu*perc_green_gas/100.#gg stands for green gas
    
    #costs green gas (TWh*€/MWh = M€)
    costs_gg=Ngas_indu_result_gg*150#69.2#€/MWh source: IRENAwww.irena.org/costs/Transportation/Biomethane
#    print('el_dem_indu', el_dem_indu)
#    print('Ngas_indu_tot',Ngas_indu_tot)
#    print('costs_gg', costs_gg)

    nam = ('input_fuel_CSHP[1]',)
    nam = nam + ('input_fuel_CSHP[2]',)
    nam = nam + ('input_fuel_CSHP[3]',)
    nam = nam + ('input_fuel_CSHP[4]',)
    nam = nam + ('Input_el_demand_Twh',)
#        print(names_var)
    values_var=[]
    values_var.append(Coal_indu)
    values_var.append(Oil_indu)
    values_var.append(Ngas_indu_tot)
    values_var.append(Bio_indu)
    values_var.append(el_demand)
    return nam, values_var, costs_gg

def EV(el_vehicles, data, diesel_kWh_on_100km, petrol_kWh_on_100km, gpl_kWh_on_100km, el_kWh_on_100km):#biofuels_TWh
#    freight_perc=29#%https://www.iea.org/data-and-statistics/charts/energy-consumption-in-transport-in-iea-countries-2018
#    passenger_perc=100-freight_perc
    perc_switch=el_vehicles
    
    diesel= data['input_fuel_Transport[2]']*(1-perc_switch/100.)
    petrol= data['input_fuel_Transport[5]']*(1-perc_switch/100.)     
    GPL= data['input_fuel_Transport[9]']*(1-perc_switch/100.)
    methane= data['input_fuel_Transport[3]']*(1-perc_switch/100.)
    
    el_transport=(data['input_fuel_Transport[2]']*el_vehicles/100.*el_kWh_on_100km/diesel_kWh_on_100km + 
                  data['input_fuel_Transport[5]']*el_vehicles/100.*el_kWh_on_100km/petrol_kWh_on_100km + 
                  data['input_fuel_Transport[9]']*el_vehicles/100.*el_kWh_on_100km/gpl_kWh_on_100km + 
                  data['input_fuel_Transport[3]']*el_vehicles/100.*el_kWh_on_100km/gpl_kWh_on_100km)/0.9
                  
    
   
    nam = ('input_fuel_Transport[2]',)
    nam = nam + ('input_fuel_Transport[5]',)
    nam = nam + ('input_fuel_Transport[9]',)
    nam = nam + ('input_fuel_Transport[3]',)
    nam = nam + ('input_transport_TWh_V2G',)
    # nam = nam + ('input_fuel_Transport[6]',)#hydrogen
    # nam = nam + ('Input_BioPetrolInput',)
#        print(names_var)
    values_var=[]
    values_var.append(diesel)
    values_var.append(petrol)
    values_var.append(GPL)
    values_var.append(methane)
    values_var.append(el_transport)
    # values_var.append(H2_transport)
    # values_var.append(biofuel)

    i=data['input_Interest']/100.
    lifetime_EVinfrastr=20.
    
    if el_vehicles==0:
        overall_costs=0.
    else:
        overall_costs=216*el_transport+46.025
#    print(colored(overall_costs, 'magenta'))
    costsEV=overall_costs*i/(1-(1+i)**(-lifetime_EVinfrastr))
#    print(colored(costsEV, 'magenta'))
    
    return nam, values_var, costsEV


#------------------------------------INPUT DATA--------------------------------

data = {"EnergyPLAN folder": r"C:\Users\MPrina\ZipEnergyPLAN161",
        "Input file": r"C:\Users\MPrina\TRUSTPV\ITALY\input_folder\IT_2030_ANSI.txt",
        "Output folder": r"C:\Users\MPrina\TRUSTPV\ITALY\input_folder",
        "Number of process": 1,
        "Genetic algorithm": {"Size of population": 4,#200
                                "Number of generations": 1},#50

        "Variables": [{"EnergyPLAN Name": "input_RES1_capacity", "Range": [11, 68],"Moltiplication factor": 1000},#onshore
                      {"EnergyPLAN Name": "input_RES2_capacity", "Range": [0, 46],"Moltiplication factor": 1000},#offshore
                      {"EnergyPLAN Name": "input_RES3_capacity", "Range": [16, 178],"Moltiplication factor": 1000},#rooftop PV
                      {"EnergyPLAN Name": "input_RES5_capacity", "Range": [5, 119],"Moltiplication factor": 1000},#US PV
                      {"EnergyPLAN Name": "input_storage_pump_cap", "Range": [0, 50],"Moltiplication factor": 10},#Batteries
                      {"EnergyPLAN Name": "input_cap_pump_el2", "Range": [0, 50],"Moltiplication factor": 1000},#Electrolyzer
                      {"EnergyPLAN Name": "input_cap_turbine_el2", "Range": [0, 50],"Moltiplication factor": 1000},#Fuel cell
                      {"EnergyPLAN Name": "input_storage_pump_cap2", "Range": [0, 50],"Moltiplication factor": 10},#H2 storage
                      {"EnergyPLAN Name": 'input_HH_HP_heat', "Range": [0, 10],"Moltiplication factor": 10.},#heat pumps
                      {"EnergyPLAN Name": 'alfa', "Range": [0 , 12],"Moltiplication factor": 5.},#energy efficiency
                      # {"EnergyPLAN Name": 'IND_el', "Range": [0 , 10],"Moltiplication factor": 10.},#industry electrification
                      # {"EnergyPLAN Name": 'IND_green_gas', "Range": [0 , 10],"Moltiplication factor": 10.} #industry green gases bought
                      ]
        }

                
#------------------------------------INITIALIZING------------------------------
VARIABLES = tuple([dic['EnergyPLAN Name'] for dic in data["Variables"]])

X = [tuple(dic['Range']) for dic in data["Variables"]]
MOLT_FACTORS = [dic['Moltiplication factor'] for dic in data["Variables"]]
NPOP= data['Genetic algorithm']["Size of population"]
NGEN= data["Genetic algorithm"]["Number of generations"]

INPUTFILE = data["Input file"]
ENERGYPLAN = data["EnergyPLAN folder"]
OUT_FOLDER = data["Output folder"]
#--------------------------------------
collection={}
c=[]
b=[]
#--------------------------------CORRECT CURVE ENERGY EFFICIENCY---------------
# Tot_Residential= 4.6*1000000000/0.85 #TWh
# Tot_Residential= 4.26*1000000000/0.85 #TWh
Tot_Residential= 361.66*1000000000/0.77 #TWh
f1= func_EF_costs(Tot_Residential, av_eff=0.77)


def f(individual):
    print('------------------------------------')
    INPUTFILE = data["Input file"]
    ENERGYPLAN = data["EnergyPLAN folder"]
    OUT_FOLDER = data["Output folder"]

    START = Node(INPUTFILE, ENERGYPLAN, OUT_FOLDER)
    new_data = START.data
    varEP = [i*j for i,j in list(zip(MOLT_FACTORS, individual))]
    
    names_var, varTH, Costs_en_eff_resid = En_Eff(INPUTFILE, OUT_FOLDER, ENERGYPLAN, varEP[-2], varEP[-1], f1, DHW=25, Heat=125)

    # perc_el_ind = varEP[-2]
    # perc_green_gas = varEP[-1]

    varEP=varEP[:-1]
    
    names=VARIABLES[:-1]+VarCosts+names_var
    for a in range(len(varEP_Costs)):
        varEP.append(varEP_Costs[a])
        
    for a in range(len(varTH)):
        varEP.append(varTH[a])
    

    # namIND, ValIND, costs_gg = Indust_new(Perc_Ind_eff= 10, data=new_data, perc_el_ind=perc_el_ind, perc_green_gas=perc_green_gas)
    # # print(namIND, ValIND)
    # names= names + namIND
    
    # for a in range(len(ValIND)):
    #     varEP.append(ValIND[a])
        
    namEV, ValEV, costsEV = EV(el_vehicles= 25,   data= new_data, 
                               diesel_kWh_on_100km=46.11, petrol_kWh_on_100km=52.78, 
                               gpl_kWh_on_100km=60.1, el_kWh_on_100km=13.61)
    
    # varEP[5]=varEP[5]+P_electrolyser
#    print('electrolyser', varEP[5])
    
    
    names= names + namEV
    for a in range(len(ValEV)):
        varEP.append(ValEV[a])
    
    for i, key in enumerate(names):
        new_data[key] = varEP[i]
#    print(VARIABLES, varEP)
#    print('transport post', new_data['input_fuel_Transport[2]'], new_data['input_fuel_Transport[5]'], new_data['input_fuel_Transport[9]'], new_data['input_fuel_Transport[3]'], new_data['input_transport_TWh_V2G'], new_data['input_fuel_Transport[6]'])

    INPUTFILE = INPUTFILE.replace('.txt','new_node'+'.txt')
    out_file = r'%s\out_new.txt' % (OUT_FOLDER)

    new_node = Node(INPUTFILE, ENERGYPLAN, out_file, new_data)
    print (colored(new_data["input_Inv_PV"], 'magenta'))
    name_ind='_'.join(map(str, individual))
    print (colored(name_ind, 'yellow'))

    if name_ind in collection:
        b.append(1)
        print (colored('a simulation saved, n = %d' %len(b), 'red'))
        dic = collection[name_ind]
        #print (len(collection))             
    else:
        new_node.write_input()
        new_node.excute()
#        print(new_node)
        # dic = new_node.read_output_y()
        dic = new_node.read_All_outputs()
        # dich=new_node.read_hourly_values()
        # dic_costs=new_node.read_costs_tech()
        
        # print(dic)
        c.append(1)
        print('a simulation executed, n = %d' %len(c))
        # collection[name_ind] = dic #new_node
    
#------------------------------------------------------------------------------
    Costs = dic['TOTAL ANNUAL COSTS']+ Costs_en_eff_resid+ costsEV+ costs_gg# + dic['PP Electr.']*45-dic['PP Electr.']*12.24 - dic['Export Electr.']*35+ Costs_en_eff_resid + costs_gg+ costsEV# + dic['Import Electr.']*200 - dic['Import Payment'] 

    CO2 = dic['CO2-emission (total)'] +15.7*0.056*1/3+ 0.5*0.557*1/3 + 22.8*0.056*1/3# +dic['CO2-emission (total)']*0.170-dic['PP Electr.']*0.353999716#+ dic['Import Electr.']*0.170 # CO2 [kt]
    
    #constraint on Electrolyser
    # Min_cap_Electrolyser=45 #MW each 0.05 TWh of generated hydrogen
    # if varEP[5]<Min_cap_Electrolyser/0.05*varEP[4]:
    #     Costs=100000
        
    # if VarEND[1]==0 and VarEND[0]!=0:
    #     Costs=100000

    # if VarEND[1]<30 and VarEND[0]!=100:
    #     Costs=100000
        
    # if perc_el_ind + perc_green_gas>100:
    #     Costs=100000000
    
#    print('CO2', dic['CO2-emission (total)'] , dic['Import Electr.']*0.170)
#    print('Costs', dic['TOTAL ANNUAL COSTS'] , dic['Import Electr.']*200)
    
#    CEEP= dic['CO2-emission (total)']
    
#    CEEP= dic['CO2-emission (total)']
    print('Costs:', colored(Costs, 'magenta'), '[M€]', type(Costs))
    print('CO2:', colored(CO2, 'cyan'), '[Mt]', type(CO2))
#    print('CEEP:', colored(CEEP, 'blue'), '[kt]')
    return CO2, Costs


    
objectives = (-1.0, -1.0,)
pop, ff, hist = GA(X, f, objectives, NPOP, NGEN)
#if __name__ == "__main__":

#pop, ff, hist = testEP()

print ('...............................................')
print(hist)

#-----------------------SAVE RESULTS ON A .csv---------------------------------
hist_file = open('history_csv.csv', 'w')
for i in range(len(VARIABLES)):
    hist_file.write(str(VARIABLES[i]) + ',')
hist_file.write('CO2 emissions [Mt]'+ ',')
hist_file.write('Total annual costs [Meuro]'+ ',')
#hist_file.write('CEEP [TWh]'+ ',')
hist_file.write('\n')
for a in range(len(hist['population'])):
    for b in range(len(hist['population'][0])):
        for c in range(len(hist['population'][0][0])):
            hist_file.write(str(hist['population'][a][b][c]*MOLT_FACTORS[c]) + ',')
        for d in range(len(hist['fitness'][0][0])):
            hist_file.write(str(hist['fitness'][a][b][d]) + ',')
        hist_file.write('\n')
hist_file.close()


#-----------------------CALCULATE AND PRINT TIME OF THE SIMULATION-------------
t1 = time.time()

total = t1-t0
print ("The total time is.. [min] ", total/60)
print ("the time per individual is...[sec] ", (float(total)/(float(NPOP*NGEN))))