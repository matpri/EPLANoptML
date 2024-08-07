# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 17:15:48 2016

@author: MPrina
"""
from libeplan import Node
import pandas as pd
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from termcolor import colored
import matplotlib as mpl
from matplotlib import pylab

#from termcolor import colored
'''max_res = [kWh]
   av_eff= average efficiency'''
def func_EF_costs(max_res, av_eff):
    xl = pd.ExcelFile("EnEffCurve.xlsx")
    # df = xl.parse("Curve")
    df = xl.parse("Sheet1")
    
    x=list(df['Energy saving (%, cumulative)'])
    #print(x)
    y=list(df['Specific cost (Euro per annual kWh saved)'])
    x=list(df['Energy saving (%, cumulative)']*max_res/100)
#    print(x)
    f1 = interp1d(x, y, kind='nearest')
    y_tot=[]
    y_cum=[]
    for a in range(len(x)):
        if a==0:
            y_tot.append(0)
            y_cum.append(0)
        else:
            y_tot.append(y[a]*(x[a]-x[a-1]))
            y_cum.append(y_cum[-1]+y_tot[-1])
    x_mod=list(df['Energy saving (%, cumulative)']*max_res/100*av_eff)
    f1 = interp1d(x_mod, y_cum, kind='linear')
    return f1#, x_mod, y_cum

'''inputfile, out_folder, energyPLAN=general input EPLANopt
    Hp = percentage given by individual [%]
    en_eff = percentage given by individual [%]
    DHW = usually 25 [kWh/m2*y]
    Heat = Heat demand of the average building [kWh/m2*y] (125 for South Tyrol)
    av_eff= average efficiency
    '''
def En_Eff(inputfile, out_folder, energyPLAN, Hp, en_eff, p, DHW, Heat):
    START = Node(inputfile, energyPLAN, out_folder)
    new_data = START.data

    alfa= en_eff

    DHW_DH = DHW/(Heat+DHW)*new_data['input_dh_ann_gr2']*(1-new_data['input_dh_ann_loss_gr2'])
    
    DH_for_en_eff=new_data['input_dh_ann_gr2']*(1-new_data['input_dh_ann_loss_gr2'])- DHW_DH
    Ind_for_en_eff=(new_data['input_fuel_Households[1]']*new_data['input_HH_coalboiler_eff'] +
                   + new_data['input_fuel_Households[2]']*new_data['input_HH_oilboiler_eff'] + new_data['input_fuel_Households[3]']*new_data['input_HH_ngasboiler_eff']
                   + new_data['input_fuel_Households[4]']*new_data['input_HH_bioboiler_eff'] + new_data['input_HH_HP_heat'] + new_data['input_HH_EB_heat'])
    
    DH_prod = (DH_for_en_eff*(1.-alfa/100.) + DHW_DH)/(1-new_data['input_dh_ann_loss_gr2'])
    coal_prod = new_data['input_fuel_Households[1]']*new_data['input_HH_coalboiler_eff']*(1.-alfa/100.)
    oil_prod = new_data['input_fuel_Households[2]']*new_data['input_HH_oilboiler_eff']*(1.-alfa/100.)
    NG_prod = new_data['input_fuel_Households[3]']*new_data['input_HH_ngasboiler_eff']*(1.-alfa/100.)
    Bio_prod = new_data['input_fuel_Households[4]']*new_data['input_HH_bioboiler_eff']*(1.-alfa/100.)   
    Old_heat_pumps_prod = new_data['input_HH_HP_heat']*(1.-alfa/100.)
    elctric_heating_prod = new_data['input_HH_EB_heat']*(1.-alfa/100.)

    How_much_en_eff_HPS=(new_data['input_fuel_Households[1]']*new_data['input_HH_coalboiler_eff'] + 
                         + new_data['input_fuel_Households[2]']*new_data['input_HH_oilboiler_eff'] +
                         + new_data['input_fuel_Households[3]']*new_data['input_HH_ngasboiler_eff'] +
                         + new_data['input_fuel_Households[4]']*new_data['input_HH_bioboiler_eff'] + 
                         + new_data['input_HH_EB_heat'])#+ new_data['input_HH_HP_heat'])
    alfa_max=75.
    HPs_individual = ((How_much_en_eff_HPS) * (1-alfa_max/100.))*(alfa/alfa_max) * Hp/100.

    coal_boiler= 0.
    oil_boiler= 0.
    electric_heat =0.
    NG_boiler= 0.
    Bio_boiler= 0.
    # print('----------')
    # print(HPs_individual, coal_prod,oil_prod,NG_prod,Bio_prod,elctric_heating_prod)
    # print('----------')
    
    
    if HPs_individual>(coal_prod+oil_prod+NG_prod+Bio_prod+elctric_heating_prod):
        HPs_individual=(coal_prod+oil_prod+NG_prod+Bio_prod+elctric_heating_prod)
        
    if HPs_individual<=coal_prod:
        coal_boiler=(coal_prod - HPs_individual)/new_data['input_HH_coalboiler_eff']
        # print(coal_boiler)
        oil_boiler = oil_prod/new_data['input_HH_oilboiler_eff']
        electric_heat = elctric_heating_prod
        NG_boiler = NG_prod/new_data['input_HH_ngasboiler_eff']
        Bio_boiler = Bio_prod/new_data['input_HH_bioboiler_eff']
        
    if HPs_individual>coal_prod and HPs_individual<=(coal_prod+oil_prod):
        coal_boiler=0.
        oil_boiler = (oil_prod - (HPs_individual-coal_prod))/new_data['input_HH_oilboiler_eff']
        electric_heat = elctric_heating_prod
        NG_boiler = NG_prod/new_data['input_HH_ngasboiler_eff']
        Bio_boiler = Bio_prod/new_data['input_HH_bioboiler_eff']
        
    if HPs_individual> (coal_prod+oil_prod) and HPs_individual<=(coal_prod + elctric_heating_prod + oil_prod):# and individual[-2]<500.+ 2246.4:
        coal_boiler= 0.        
        oil_boiler = 0.
        electric_heat = (elctric_heating_prod- (HPs_individual - oil_prod -coal_prod))
        NG_boiler = NG_prod/new_data['input_HH_ngasboiler_eff'] #max(0, NG_prod + oil_prod - HPs_individual)
        Bio_boiler = Bio_prod/new_data['input_HH_bioboiler_eff']
        
    if HPs_individual> (coal_prod+oil_prod+ elctric_heating_prod) and HPs_individual<=(coal_prod+NG_prod + oil_prod + elctric_heating_prod):# and individual[-2]<500.+ 2246.4:
        coal_boiler= 0.        
        oil_boiler = 0.
        electric_heat =0.
        NG_boiler = (NG_prod - (HPs_individual - elctric_heating_prod - oil_prod -coal_prod))/new_data['input_HH_ngasboiler_eff'] #max(0, NG_prod + oil_prod - HPs_individual)
        Bio_boiler = Bio_prod/new_data['input_HH_bioboiler_eff']
        
    if HPs_individual>(coal_prod+NG_prod + oil_prod + elctric_heating_prod):
        coal_boiler= 0.
        oil_boiler = 0.
        electric_heat =0.
        NG_boiler = 0.
        Bio_boiler = (Bio_prod - (HPs_individual - oil_prod - NG_prod -coal_prod - elctric_heating_prod))/new_data['input_HH_bioboiler_eff']
    
    HPs_individual= HPs_individual + Old_heat_pumps_prod

    names_var=('input_dh_ann_gr2', 'input_fuel_Households[1]','input_fuel_Households[2]', 'input_HH_EB_heat', 'input_fuel_Households[3]', 'input_fuel_Households[4]', 'input_HH_HP_heat')
    # print('----------')
    #-------------------------------------------COSTS EN EFF-------------------
    i=new_data['input_Interest']/100.
    lifetime_eff_ener=35.
    
    annual_kWh_saved = (DH_for_en_eff+ Ind_for_en_eff)*alfa/100.*1000000000#[kWh]
#    print('max efficientabile:', (DH_for_en_eff+ Ind_for_en_eff))
#    print(colored(annual_kWh_saved, 'blue'))
    if alfa==0.:
        Costs_en_eff_resid=0.
    else:
        Costs_en_eff_resid= p(annual_kWh_saved)/1000000.*i/(1-(1+i)**(-lifetime_eff_ener)) #M€
        
#    print('Costs_en_eff_resid', colored(Costs_en_eff_resid, 'magenta'))
#    print(p(annual_kWh_saved))
    #--------------------------------------------------------------------------
#    print([DH_prod, coal_boiler, oil_boiler, electric_heat, NG_boiler, Bio_boiler, HPs_individual])
    return names_var, [DH_prod, coal_boiler, oil_boiler, electric_heat, NG_boiler, Bio_boiler, HPs_individual], Costs_en_eff_resid


# data = {"EnergyPLAN folder": r"C:\Users\MPrina\Desktop\ZipEnergyPLAN151",
#         # "Input file baseline": r"C:\Users\MPrina\Desktop\Salzburg\EPLANopt\input_folder\Salzburg_costs_2015_ANSI.txt",
#         "Input file": r"C:\Users\MPrina\Desktop\Salzburg\2030\EPLANopt - 25EV - mod\input_folder\Salzburg_2030_DH_ANSI.txt",
#         "Output folder": r"C:\Users\MPrina\Desktop\Salzburg\2030\EPLANopt - 25EV - mod\input_folder",
#         "Number of process": 1,
#         "Genetic algorithm": {"Size of population": 100,
#                                 "Number of generations": 50},

#         "Variables": [{"EnergyPLAN Name": "input_RES1_capacity", "Range": [1, 20],"Moltiplication factor": 50},
#                       {"EnergyPLAN Name": "input_RES2_capacity", "Range": [1, 9],"Moltiplication factor": 50},
#                       {"EnergyPLAN Name": "input_RES4_capacity", "Range": [0, 5],"Moltiplication factor": 50},
#                       {"EnergyPLAN Name": "input_storage_pump_cap", "Range": [0, 10],"Moltiplication factor": 10},
#                       {"EnergyPLAN Name": 'Input_CO2HydroSynGridGas', "Range": [0, 9],"Moltiplication factor": 0.05},
#                       {"EnergyPLAN Name": 'input_cap_ELTtrans_el', "Range": [0, 10],"Moltiplication factor": 50},
#                       {"EnergyPLAN Name": 'input_H2storage_trans_cap', "Range": [0, 10],"Moltiplication factor": 5},
#                       {"EnergyPLAN Name": 'input_HH_HP_heat', "Range": [0, 10],"Moltiplication factor": 10.},
#                       {"EnergyPLAN Name": 'alfa', "Range": [0 , 15],"Moltiplication factor": 5.}] #[0, 75]
#         }
                
# #------------------------------------INITIALIZING------------------------------
# VARIABLES = tuple([dic['EnergyPLAN Name'] for dic in data["Variables"]])

# X = [tuple(dic['Range']) for dic in data["Variables"]]
# MOLT_FACTORS = [dic['Moltiplication factor'] for dic in data["Variables"]]
# NPOP= data['Genetic algorithm']["Size of population"]
# NGEN= data["Genetic algorithm"]["Number of generations"]

# INPUTFILE = data["Input file"]
# ENERGYPLAN = data["EnergyPLAN folder"]
# OUT_FOLDER = data["Output folder"]
# ## ------------------------------------INITIALIZING-----------------------------

# START = Node(INPUTFILE, ENERGYPLAN, OUT_FOLDER)
# new_data = START.data
# # en_eff=[i for i in range(75)]

# Tot_Residential= 4.26*1000000000/0.85 #TWh
# # Tot_Residential= 4.34*1000000000 #TWh
# f2= func_EF_costs(Tot_Residential, av_eff=0.85)

# # # Tot_Residential= 4.26*1000000000/0.85 #TWh
# # # f1= func_EF_costs(Tot_Residential, av_eff=0.85)
# # ##
# # #list_costs=[]
# # list_oil=[]

# # for a in range(len(en_eff)):
# #     names_var, gigi, Cost_En_Eff = En_Eff(INPUTFILE, OUT_FOLDER, ENERGYPLAN, 100,  en_eff[a], f1, DHW=25, Heat=125)
# #     list_oil.append(gigi[2])
# #     # list_costs.append(Cost_En_Eff)
# # print(list_oil)
# eff_list=[]
# en_eff1=[i*5 for i in range(12)]
# #en_eff1=[10.]
# y1 = []
# y2 = []
# y3 = []
# y4 = []
# y5 = []
# y6 = []
# y7 = []
# for a in range(len(en_eff1)):
#     names_var, varTH, Costs_en_eff_resid = En_Eff(INPUTFILE, OUT_FOLDER, ENERGYPLAN, 100., en_eff1[a], f2, 25, 125)
#     eff_list.append(Costs_en_eff_resid)
#     y1.append(varTH[0])#DH_prod
#     y2.append(varTH[1])#coal_boiler
#     y3.append(varTH[2])#oil_boiler
#     y4.append(varTH[3])#elctric_heating_prod
#     y5.append(varTH[4])#NG_boiler
#     y6.append(varTH[5])#Bio_boiler
#     y7.append(varTH[6])#HPs_individual
# #    
# ##------------------------------PLOT--------------------------------------------
# ##x=[i+1 for i in range(len(y))]
# fig, ax = plt.subplots()

# ax.plot(en_eff1, eff_list, c= 'blue')

# ax.set_xlabel('energy efficiency')
# ax.set_ylabel('costs en eff [MEuro]')

# #pylab.xlim([0, 100])

# plt.grid()
# plt.show()
# ##------------------------------PLOT--------------------------------------------
# fig2, ax = plt.subplots()

# y=[y1, y2, y3, y4, y5, y6, y7]
# #red_line, = axes[a][0].plot(x, y_demand, color='red', linewidth=width, label='Demand')
# sp = ax.stackplot(en_eff1, y, colors=('moccasin', 'black','chocolate', 'cyan' , 'yellow', 'green', 'plum'), alpha=0.8, linewidth=0.35, edgecolor='black')
# ax.set_ylabel('Energy \nconsumption [TWh]', fontsize=10)
# ax.set_xlabel('Energy efficiency [%]', fontsize=10)
# ax.grid(linestyle='dotted')
# art = []
# handles = [mpl.patches.Rectangle((0,0), 0,0, facecolor=pol.get_facecolor()[0]) for pol in sp]
# #handles.append(red_line)
# labelsENG=('District heating', 'Coal boilers', 'Oil boilers','Electric boilers', 'Natural gas boilers','Biomass boilers','Heat pumps')
# labels=('Fernwärme', 'Kohle Brennkessel', 'Heizöl Brennkessel','Elektrische Kessel', 'Erdgas Brennkessel','Biomasse Brennkessel','Wärmepumpen')
# lgd = pylab.legend(reversed(handles), reversed(labelsENG), bbox_to_anchor=(1.01, 0.5), loc='center left', ncol=1)#bbox_to_anchor=(1.01, 2.9), loc='center left', borderaxespad=0., ncol=1, fontsize=13
# art.append(lgd)
# pylab.savefig("En_eff.png", additional_artists=art, bbox_inches="tight", dpi=300)

