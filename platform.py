# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:44:48 2022

@author: 12427
"""

import streamlit as st
import pandas as pd
import myfunction
import streamlit.components.v1 as components
from datetime import datetime
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

@st.cache(suppress_st_warning=True, max_entries = 5,ttl = 24*3600)
def load_data():
    researchDf = pd.read_pickle('data/researchDf.pkl')
    birthInfo = pd.read_pickle('data/birthInfo.pkl')
    birthInfo.rename(columns = {'birthtime':'time'}, inplace = True)
    df = researchDf.copy()
    return researchDf, birthInfo, df

researchDf, birthInfo, df = load_data()

def selectSubCategory(inputdf, colName):
    DfDict = {}
    catDict = {f"{len(inputdf['adb_id'].unique())} persons)": "All"}
    mycatList = [f"{len(inputdf['adb_id'].unique())} persons)"]
    for name,subDf in inputdf.groupby(colName):
        DfDict[name] = subDf
        catDict[f"{name} ({len(subDf['adb_id'].unique())} persons)"] = name
        if subDf.shape[0]>0:
            mycatList.append(f"{name} ({len(subDf['adb_id'].unique())} persons)")
    #mycatList = researchDf['category'].unique()
    return DfDict, catDict, mycatList

# =============================================================================
# researchDfDict = {}
# catDict = {}
# mycatList = []
# for i,j in researchDf.groupby('category'):
#     researchDfDict[i] = j
#     catDict[f"{i} ({j.shape[0]} items available)"] = i
#     mycatList.append(f"{i} ({j.shape[0]} items available)")
# =============================================================================
#mycatList = researchDf['category'].unique()

researchDfDict, catDict, mycatList = selectSubCategory(df, "category")
category = st.selectbox('Which Category Are You Looking for?', mycatList)
#df = researchDf[researchDf['category'] == category]
if catDict[category] == 'All':
    pass
else:
    df = researchDfDict[catDict[category]]
    #df = df[~df['person'].duplicated()]
#df = researchDfDict[catDict[category]]
#df = df[~df['person'].duplicated()]

#mysubcatList = ['All']
#mysubcatList.extend(df['subcategory'].unique())
researchDfDict, catDict, mysubcatList = selectSubCategory(df, "subcategory")
subcategory = st.selectbox('Which Subcategory Are You Looking for?', mysubcatList)
if catDict[subcategory] == 'All':
    pass
else:
    df = researchDfDict[catDict[subcategory]]
    #df = df[~df['person'].duplicated()]


#mydetailList = ['All']
#mydetailList.extend(df['detail'].unique())
researchDfDict, catDict, mydetailList = selectSubCategory(df, "detail")
detail = st.selectbox('Which Detail Are You Looking for?', mydetailList)

if catDict[detail] == 'All':
    pass
else:
    #df = df[df['detail'] == detail]
    df = researchDfDict[catDict[detail]]
    df = df[~df['person'].duplicated()]

nonDupDf = df[~df['adb_id'].duplicated()]
#nonDupDf.sort_values(by=['adb_id'], inplace = True)
nonDupDf = nonDupDf[['adb_id','person', 'As_sign', 'Sun_sign']]

nonDupDf.reset_index(drop = True, inplace = True)
selectDf = nonDupDf[['person', 'As_sign', 'Sun_sign']]
#st.dataframe(nonDupDf[['person', 'As_sign', 'Sun_sign']])

# =============================================================================
# selected_indices = st.multiselect('Select rows:', nonDupDf.index)
# selected_rows = nonDupDf.loc[selected_indices]
# st.write('### Selected Rows', selected_rows)
# =============================================================================
selectDf = selectDf.merge(birthInfo, on = 'adb_id')
selectDf.drop(columns = ['adb_id'], inplace = True)
gd = GridOptionsBuilder.from_dataframe(selectDf)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gridoptions = gd.build()

select_person, chart = st.columns(2)

with select_person:
    grid_table = AgGrid(selectDf, height=400, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED)

with chart:
   birth2 = datetime(2023, 1, 1 , 0, 0)
   info2 = ["Irvine", "US", birth2]
   try:
       selected_row = grid_table["selected_rows"]
       birth2 = datetime.fromisoformat(selected_row[0]['time'][:-1])
       info2 = [selected_row[0]['place'], selected_row[0]['country'], birth2]
       #res = myfunction.JSreadable(myfunction.getAllinfo(*info2))
   except:
       pass
   #st.write(info2)
   res = myfunction.JSreadable(myfunction.getAllinfo(*info2))
   astrodata = "const data = " + str(res)

   location = "chartHtml/radix.html"
   #location = "testHtml.html"
   HtmlFile = open(location, 'r', encoding='utf-8')
   source_code = HtmlFile.read() 

   location2 = "chartHtml/astrochart.js"
   HtmlFile2 = open(location2, 'r', encoding='utf-8')
   astroChartFunction = HtmlFile2.read() 
   astroChartFunction = "<script>\n" + astroChartFunction + "\n</script>"
   #print(astroChartFunction)

   source_code = source_code.replace('<script src="../../build/astrochart.js"></script>', astroChartFunction)
   source_code = source_code.replace("var radix = new astrology.Chart('paper', 600, 600).radix( data );", 
                                     "var radix = new astrology.Chart('paper', 400, 400).radix( data );")
   
   source_code = source_code.replace('const data = [0]', astrodata)

   #print(type(source_code))
   components.html(source_code, height=400, scrolling= True)



# =============================================================================
# data = {
#     'country': ['Japan', 'China', 'Thailand', 'France', 'Belgium', 'South Korea'],
#     'capital': ['Tokyo', 'Beijing', 'Bangkok', 'Paris', 'Brussels', 'Seoul']
# }
# 
# df = pd.DataFrame(data)
# gd = GridOptionsBuilder.from_dataframe(df)
# gd.configure_selection(selection_mode='multiple', use_checkbox=True)
# gridoptions = gd.build()
# 
# grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
#                     update_mode=GridUpdateMode.SELECTION_CHANGED)
# 
# st.write('## Selected')
# selected_row = grid_table["selected_rows"]
# st.dataframe(selected_row)
# =============================================================================

myvarList = [' ']
myvarList.extend(list(researchDf.columns))
remove_item = ['person','adb_id','Key','name','category',
               'subcategory','detail','comment']
myvarList = [e for e in myvarList if e not in remove_item]
myvar = st.selectbox('Which Variable Are You Looking for?', myvarList)

try:
    showedDf = pd.DataFrame((df[myvar].value_counts().reset_index()))
    
    showedDf.rename(columns = {myvar:"count"}, inplace = True)
    showedDf.rename(columns = {"index":myvar}, inplace = True)
    #st.dataframe(showedDf)
    #showedDf['house'] = showedDf['house'].map(lambda x: int(x[5:]))
    total = showedDf["count"].sum()
    showedDf['total'] = total
    showedDf['percentage'] = showedDf["count"]/total
    showedDf['expected'] = 1/showedDf.shape[0]
    showedDf['difference'] = showedDf['percentage'] - showedDf['expected']
    st.dataframe(showedDf)
except:
    pass