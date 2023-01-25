# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 17:42:19 2022

@author: Chupeng Zheng
"""
import swisseph as swe
import pandas as pd


from collections import defaultdict

import pytz

from tzwhere import tzwhere
from geopy.geocoders import Nominatim

import warnings
warnings.filterwarnings("ignore")

geolocator = Nominatim(user_agent="my_request")
mytzwhere = tzwhere.tzwhere()

knowledge = pd.read_excel('./variables_profile4.xlsx', sheet_name='signs')
aspectInfo = pd.read_excel('variables_profile4.xlsx', sheet_name='aspect')
orbitInfo = pd.read_excel('variables_profile4.xlsx', sheet_name='orb')
moon_phaseInfo = pd.read_excel('variables_profile4.xlsx', sheet_name='moon_phase')
aspect_signInfo = pd.read_excel('variables_profile4.xlsx', sheet_name='aspect_sign')
dignityInfo = pd.read_excel('variables_profile4.xlsx', sheet_name='dignity2',index_col=0)
sign_order = pd.read_excel('variables_profile4.xlsx', sheet_name='sign_order')
sign_order = sign_order.iloc[:12]
bound_info = pd.read_excel('variables_profile4.xlsx', sheet_name='bound')

planet_dict = {'Sun':0, 
          'Moon':1,
          'Mercury':2,
          'Venus':3,
          'Mars':4,
          'Jupiter':5,
          'Saturn':6,
          'Uranus':7,
          'Neptune':8,
          'Pluto':9,
          'Mean_Node':10,
          'True_Node(North_Node)':11,
            'South_Node':11}


def shrinkto30(i):
    while True:
        if i < 30:
            return i
        i = i -30
        
def dict_house_info(degreefrom_sewhouses):
    output = defaultdict()
    for i in range(len(degreefrom_sewhouses[0])):
        degreei = degreefrom_sewhouses[0][i]
        output[f'house{i+1}'] = {'degree': round(degreei,3),
                                'sign': knowledge.loc[degreei//30,'sign_short'],
                                'sign_degree': round(shrinkto30(degreei),3),
                                'ruler': knowledge.loc[degreei//30,'ruler']}
    return output

def dict_planet_info(degreefrom_planet):
    output = defaultdict()
    for i,j in degreefrom_planet.items():
        degreei = j
        output[i] = {'degree': round(degreei,3),
                    'sign': knowledge.loc[degreei//30,'sign_short'], 
                    'sign_degree': round(shrinkto30(degreei),3),
                    'ruler': knowledge.loc[degreei//30,'ruler']}
    return output

def gethouse_and_planet_info(location,utc_dt):
   
    jd = swe.utc_to_jd(utc_dt.year,utc_dt.month,utc_dt.day,utc_dt.hour,utc_dt.minute,seconds= 0,flag = 1)
    res = swe.houses(jd[1],location.latitude,location.longitude)
    houseinfo = dict_house_info(res)
    planet = {}
    for i,j in planet_dict.items():
        try:
            planet[i] = swe.calc_ut(jd[1],j)[0][0]
        except:
            continue

    if planet['True_Node(North_Node)']<180:
        planet['South_Node'] = planet['True_Node(North_Node)']+180
    else:
        planet['South_Node'] = planet['True_Node(North_Node)']-180
    planet['As'] = houseinfo['house1']['degree']
    planet['Ds'] = houseinfo['house7']['degree']
    planet['Ic'] = houseinfo['house4']['degree']
    planet['MC'] = houseinfo['house10']['degree']
    return utc_dt, houseinfo, planet


# input: place, country and time
# output: all house and planets' position info
def getAllinfo(place, county, birthtime):
    try:
        location = geolocator.geocode(str(place)+', '+str(county))
        timezone_str = mytzwhere.tzNameAt(location.latitude,location.longitude)
        #print(str(place)+', '+str(county))
        local = pytz.timezone(timezone_str)
        local_dt = local.localize(birthtime, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        print(utc_dt)
        
        return gethouse_and_planet_info(location,utc_dt)
    except:
        try:
            location = geolocator.geocode(str(county))
            timezone_str = mytzwhere.tzNameAt(location.latitude,location.longitude)
        #print(str(place)+', '+str(county))
            local = pytz.timezone(timezone_str)
            local_dt = local.localize(birthtime, is_dst=None)
            utc_dt = local_dt.astimezone(pytz.utc)
            return gethouse_and_planet_info(location,utc_dt)
        
        except:
            location = geolocator.geocode(str(county))
            utc_dt = birthtime
            return 'timezone not found, utc used defaultly',gethouse_and_planet_info(location,local_dt)

# no longer used        
def cal_diff(infoListA, infoListB):
    planetA = getAllinfo(*infoListA)[-1]
    planetB = getAllinfo(*infoListB)[-1]
    
    for i, j in planetA.items():
        print('---------------------------------------------')
        for m,n in planetB.items():
            diff = j - n
            if diff < 0:
                res = 360 + diff
            else:
                res = diff
            print(f'The difference of input A\'s {i} and B\'s {m} is {res}')
     
# save the data in Javascript style, so Kibo's code can use it.            
def JSreadable(fromgetAllinfo):
    pl = fromgetAllinfo[-1]
    cu = fromgetAllinfo[1]
    
    cusps = []
    house1 = (cu['house1']['degree']//30)*30
    hh = house1
    for i in range(12):
        if hh > 360:
            hh = hh -360
        cusps.append(hh)
        hh = hh + 30

    planets = {"Pluto":[pl['Pluto']], "Neptune":[pl['Neptune']],#"Neptune":[305.1, 0.2], 
        "Uranus":[pl['Uranus']], "Saturn":[pl['Saturn']],#"Saturn":[54.9, -0.2], 
        "Jupiter":[pl['Jupiter']], "Mars":[pl['Mars']], "Moon":[pl['Moon']], 
        "Sun":[pl['Sun']], "Mercury":[pl['Mercury']], "Venus":[pl['Venus']], 
        "NNode":[pl['True_Node(North_Node)']]}
    AIDM = [pl['As'],0,0,pl['Ic'],0,0,pl['Ds'],0,0,pl['MC'],0,0]
    
    res = {}
    res['planets'] = planets
    res['cusps'] = cusps
    res['AIDM'] = AIDM
    
    return res

def cleanInfo(infofromPlanet):
    usefulPlanet = ['Sun',
                    'Moon',
                    'Mercury',
                    'Venus',
                    'Mars',
                    'Jupiter',
                    'Saturn',
                    'Uranus',
                    'Neptune',
                    'Pluto',
                   'True_Node(North_Node)',
                   'South_Node',
                    'As','Ds','Ic','MC']
    res = {}
    for i in usefulPlanet:
        res[i] = infofromPlanet[i]
        
    return res


# input two lists of info
# calculate position difference
def cal_diff2(infoListA, infoListB, printYes = False):
    planetA = getAllinfo(*infoListA)[-1]
    planetA = cleanInfo(planetA)
    planetB = getAllinfo(*infoListB)[-1]
    planetB = cleanInfo(planetB)
    outputphase = {}
    outputdistance = {}
    
    for i, j in orbitInfo.iterrows():
        if printYes == True:
            print('---------------------------------------------')
        for m,n in planetB.items():
            A_degree = planetA[j['planet']]
            diff =  n - A_degree
            if diff < 0:
                res = 360 + diff
            else:
                res = diff
            
            #print(res)
            aspectInfo2 = aspectInfo.copy()
            aspectInfo2['orb'] = j['orb_natal']
            aspectInfo2['from'] = aspectInfo2['exact_aspect'] - aspectInfo2['orb']
            aspectInfo2['to'] = aspectInfo2['exact_aspect'] + aspectInfo2['orb']
            for k,p in aspectInfo2.iterrows():
                #print(res)
                if res >= p['from'] and res < p['to'] and j["planet"]!= m:
                    final = f'The difference of input A\'s {j["planet"]} and B\'s {m} is {res}||{diff}, {p["aspect"]}'
                    if printYes == True:
                        print(final)
                    outputphase[j["planet"]+"_"+m] = p["aspect"]
            outputdistance[j["planet"]+"_"+m] = res
            
            #print(f'The difference of input A\'s {i} and B\'s {m} is {res}')
    return outputphase,outputdistance

# used to create asc_ruler_aspect_asc info, see following.
def cal_sign_distance(as_sign,ruler_sign):
    
    return abs(knowledge[knowledge['sign_short']==ruler_sign].index[0] - knowledge[knowledge['sign_short']==as_sign].index[0])

# create all variables
def create_variable(infoList,person_name:str, adb_id = -1):
    df = pd.DataFrame([{'person':person_name,'adb_id': adb_id}])
    myast = getAllinfo(*infoList)
    dict_planet_info_AST = dict_planet_info(myast[-1])
    
    for i, j in dict_planet_info_AST.items():
        df[i+'_sign'] = j['sign']
        #print(j['sign'])
        try:
            if pd.isnull(dignityInfo.loc[j['sign'],i]) ==True:
                df[i+'_dignity'] = 'peregrine'   
            else:
                df[i+'_dignity'] = dignityInfo.loc[j['sign'],i]
        except:
            pass
        df[i+'_element'] = knowledge[knowledge['sign_short'] == j['sign']]['element'].iloc[0]
        df[i+'_modality'] = knowledge[knowledge['sign_short'] == j['sign']]['modality'].iloc[0]
        
        bound_degree = int(j['sign_degree'])+1
        boundDF = bound_info[bound_info['sign'] == j['sign']]
        bound_planet = boundDF[(boundDF['from']<= bound_degree) & (boundDF['to'] >= bound_degree)]['planet'].iloc[0]
        df[i+'_bound'] = bound_planet

    #add difference of position between each planet
    temp_df_phase,temp_df_distance = cal_diff2(infoList, infoList)
    temp_df_phase = pd.DataFrame([temp_df_phase])
    df = pd.concat([df,temp_df_phase], axis = 1)

    #houseDegreelist = []
    for i, j in myast[-2].items():
        df[i] = j['sign']
        #houseDegreelist.append(j['degree'])
    
    #add element and modality

    for i, j in dict_planet_info_AST.items():
        #print(j)
        temp_sign = j['sign']
        HouseLoc = sign_order[sign_order['House1'] == df['house1'][0]]
        HouseLoc = list(sign_order[sign_order['House1'] == df['house1'].iloc[0]].iloc[0]).index(temp_sign) + 1
        df[i+'_house'] = 'house'+ str(HouseLoc)
    
    asc_ruler = dict_planet_info_AST['As']['ruler']
    df['as_ruler'] = asc_ruler
    df['as_ruler_element'] = df[asc_ruler+'_element'][0]
    df['as_ruler_modality'] = df[asc_ruler+'_modality'][0]
    asc_ruler_aspect_asc = cal_sign_distance(df['As_sign'].iloc[0],df[asc_ruler+"_sign"].iloc[0])
    df['as_ruler_aspect_as'] = aspect_signInfo[aspect_signInfo['count_distance_by_sign']==asc_ruler_aspect_asc].aspect.iloc[0]
    df['as_ruler_in_house'] = df[asc_ruler + '_house'].iloc[0]
    
    mc_ruler = dict_planet_info_AST['MC']['ruler']
    df['mc_ruler'] = mc_ruler
    df['mc_ruler_element'] = df[mc_ruler+'_element'][0]
    df['mc_ruler_modality'] = df[mc_ruler+'_modality'][0]
    mc_ruler_aspect_mc = cal_sign_distance(df['MC_sign'].iloc[0],df[mc_ruler+"_sign"].iloc[0])
    df['mc_ruler_aspect_mc'] = aspect_signInfo[aspect_signInfo['count_distance_by_sign']==mc_ruler_aspect_mc].aspect.iloc[0]
    df['mc_ruler_in_house'] = df[mc_ruler + '_house'].iloc[0]
    
    moon_phase = moon_phaseInfo[(moon_phaseInfo['From']< temp_df_distance['Sun_Moon']) & (moon_phaseInfo['To'] > temp_df_distance['Sun_Moon'])]['moon_phase'].iloc[0]
    df['moon_phase'] = moon_phase
    
    stellium_temp = df[df.columns[df.columns.str.contains('sign')][:10]].iloc[0].value_counts()
    stellium_temp = stellium_temp[stellium_temp>=3].index
    df[stellium_temp + '_stellium'] = 1
    return df

def create_variable_df_ver(infolist2):
    person_name = infolist2[-2]
    adb_id = infolist2[-1]
    infoList = infolist2[:3]
    df = pd.DataFrame([{'person':person_name,'adb_id': adb_id}])
    myast = getAllinfo(*infoList)
    dict_planet_info_AST = dict_planet_info(myast[-1])
    
    for i, j in dict_planet_info_AST.items():
        df[i+'_sign'] = j['sign']
        #print(j['sign'])
        try:
            if pd.isnull(dignityInfo.loc[j['sign'],i]) ==True:
                df[i+'_dignity'] = 'peregrine'   
            else:
                df[i+'_dignity'] = dignityInfo.loc[j['sign'],i]
        except:
            pass
        df[i+'_element'] = knowledge[knowledge['sign_short'] == j['sign']]['element'].iloc[0]
        df[i+'_modality'] = knowledge[knowledge['sign_short'] == j['sign']]['modality'].iloc[0]
        
        bound_degree = int(j['sign_degree'])+1
        boundDF = bound_info[bound_info['sign'] == j['sign']]
        bound_planet = boundDF[(boundDF['from']<= bound_degree) & (boundDF['to'] >= bound_degree)]['planet'].iloc[0]
        df[i+'_bound'] = bound_planet
        
    #add difference of position between each planet
    temp_df_phase,temp_df_distance = cal_diff2(infoList, infoList)
    temp_df_phase = pd.DataFrame([temp_df_phase])
    df = pd.concat([df,temp_df_phase], axis = 1)

    #houseDegreelist = []
    for i, j in myast[-2].items():
        df[i] = j['sign']
        #houseDegreelist.append(j['degree'])
    
    #add element and modality

    for i, j in dict_planet_info_AST.items():
        #print(j)
        temp_sign = j['sign']
        HouseLoc = sign_order[sign_order['House1'] == df['house1'][0]]
        HouseLoc = list(sign_order[sign_order['House1'] == df['house1'].iloc[0]].iloc[0]).index(temp_sign) + 1
        df[i+'_house'] = 'house'+ str(HouseLoc)
    
    asc_ruler = dict_planet_info_AST['As']['ruler']
    df['as_ruler'] = asc_ruler
    df['as_ruler_element'] = df[asc_ruler+'_element'][0]
    df['as_ruler_modality'] = df[asc_ruler+'_modality'][0]
    asc_ruler_aspect_asc = cal_sign_distance(df['As_sign'].iloc[0],df[asc_ruler+"_sign"].iloc[0])
    df['as_ruler_aspect_as'] = aspect_signInfo[aspect_signInfo['count_distance_by_sign']==asc_ruler_aspect_asc].aspect.iloc[0]
    df['as_ruler_in_house'] = df[asc_ruler + '_house'].iloc[0]
    
    mc_ruler = dict_planet_info_AST['MC']['ruler']
    df['mc_ruler'] = mc_ruler
    df['mc_ruler_element'] = df[mc_ruler+'_element'][0]
    df['mc_ruler_modality'] = df[mc_ruler+'_modality'][0]
    mc_ruler_aspect_mc = cal_sign_distance(df['MC_sign'].iloc[0],df[mc_ruler+"_sign"].iloc[0])
    df['mc_ruler_aspect_mc'] = aspect_signInfo[aspect_signInfo['count_distance_by_sign']==mc_ruler_aspect_mc].aspect.iloc[0]
    df['mc_ruler_in_house'] = df[mc_ruler + '_house'].iloc[0]
    
    moon_phase = moon_phaseInfo[(moon_phaseInfo['From']< temp_df_distance['Sun_Moon']) & (moon_phaseInfo['To'] > temp_df_distance['Sun_Moon'])]['moon_phase'].iloc[0]
    df['moon_phase'] = moon_phase
    
    stellium_temp = df[df.columns[df.columns.str.contains('sign')][:10]].iloc[0].value_counts()
    stellium_temp = stellium_temp[stellium_temp>=3].index
    df[stellium_temp + '_stellium'] = 1
    return df

def day_night(infolist):
    pl = getAllinfo(*infolist)[-1]
    DsPos = pl['Ds']
    if (DsPos+180)%360 < 180:
        if (pl['Sun'] < 360 and pl['Sun'] > DsPos) or (pl['Sun'] < pl['As'] and pl['Sun'] > 0):
            return 'day'
        else:
            return 'night'
    else:
        if pl['Sun'] < DsPos+180 and pl['Sun'] > DsPos:
            return 'day'
        else:
            return 'night'


# reorder the dataframe, not really necessary.
def reorderDf(df):
    col_no_ste = df.columns[~df.columns.str.contains('_stellium')]
    stellium_split = df.columns[df.columns.str.contains('_stellium')]
    
    st = list(col_no_ste).index("Sun_house")

    en = list(col_no_ste).index("moon_phase")

    
    col = list(col_no_ste[:st]) + list(col_no_ste[en+1:])+ list(col_no_ste[st:en+1]) + list(stellium_split)
    

    return df[col]