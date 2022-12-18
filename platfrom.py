# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:44:48 2022

@author: 12427
"""

import streamlit as st
import pandas as pd

researchDf = pd.read_csv('data/researchDf.csv')

mycatList = ['N/A']
mycatList.extend(researchDf['category'].unique())
category = st.selectbox('Which Category Are You Looking for?', mycatList)

df = researchDf[researchDf['category'] == category]
test = df[~df['person'].duplicated()]

st.dataframe(test)

myvarList = ['N/A']
myvarList.extend(list(researchDf.columns))
remove_item = ['person','adb_id','Key','name','category',
               'subcategory','detail','comment']
myvarList = [e for e in myvarList if e not in remove_item]
myvar = st.selectbox('Which Variable Are You Looking for?', myvarList)

try:
    showedDf = pd.DataFrame((test[myvar].value_counts().reset_index()))
    showedDf.rename(columns = {"index":'house'}, inplace = True)
    showedDf['house'] = showedDf['house'].map(lambda x: int(x[5:]))
    total = showedDf[myvar].sum()
    showedDf['percentage'] = showedDf[myvar]/total
    showedDf['total'] = total
    
    st.dataframe(showedDf)
except:
    pass