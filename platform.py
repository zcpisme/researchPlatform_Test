# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:44:48 2022

@author: 12427
"""

import streamlit as st
import pandas as pd
#import myfunction
researchDf = pd.read_pickle('data/researchDf.pkl')
df = researchDf.copy()

def selectSubCategory(inputdf, colName):
    DfDict = {}
    catDict = {f"All ({df.shape[0]} items available, {len(inputdf['adb_id'].unique())} non-duplicated)": "All"}
    mycatList = [f"All ({df.shape[0]} items available, {len(inputdf['adb_id'].unique())} non-duplicated)"]
    for name,subDf in inputdf.groupby(colName):
        DfDict[name] = subDf
        catDict[f"{name} ({subDf.shape[0]} items available, {len(subDf['adb_id'].unique())} non-duplicated)"] = name
        if subDf.shape[0]>0:
            mycatList.append(f"{name} ({subDf.shape[0]} items available, {len(subDf['adb_id'].unique())} non-duplicated)")
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
nonDupDf.sort_values(by=['adb_id'], inplace = True)
nonDupDf.reset_index(drop = True, inplace = True)

st.dataframe(nonDupDf)


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