# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:44:48 2022

@author: 12427
"""

import streamlit as st
import pandas as pd

researchDf = pd.read_csv('data/researchDf.csv')

mycatList = ['All']
mycatList.extend(researchDf['category'].unique())
category = st.selectbox('Which Category Are You Looking for?', mycatList)

if category == 'All':
    test= researchDf

else:
    df = researchDf[researchDf['category'] == category]
    #test = df[~df['person'].duplicated()]

mysubcatList = ['All']
mysubcatList.extend(test['subcategory'].unique())
subcategory = st.selectbox('Which Subcategory Are You Looking for?', mysubcatList)

if subcategory == 'All':
    pass
else:
    df = test[test['subcategory'] == subcategory]
    #test = df[~df['person'].duplicated()]

mydetailList = ['All']
mydetailList.extend(test['detail'].unique())
detail = st.selectbox('Which Detail Are You Looking for?', mydetailList)

if detail == 'All':
    pass
else:
    df = test[test['detail'] == detail]
    test = df[~df['person'].duplicated()]


st.dataframe(test)


myvarList = [' ']
myvarList.extend(list(researchDf.columns))
remove_item = ['person','adb_id','Key','name','category',
               'subcategory','detail','comment']
myvarList = [e for e in myvarList if e not in remove_item]
myvar = st.selectbox('Which Variable Are You Looking for?', myvarList)

try:
    showedDf = pd.DataFrame((test[myvar].value_counts().reset_index()))
    
    showedDf.rename(columns = {myvar:"count"}, inplace = True)
    showedDf.rename(columns = {"index":myvar}, inplace = True)
    #st.dataframe(showedDf)
    #showedDf['house'] = showedDf['house'].map(lambda x: int(x[5:]))
    total = showedDf["count"].sum()
    showedDf['percentage'] = showedDf["count"]/total
    showedDf['total'] = total
    
    st.dataframe(showedDf)
except:
    pass