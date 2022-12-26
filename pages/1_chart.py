# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:44:48 2022

@author: 12427
"""
import streamlit as st
from tzwhere import tzwhere

mytzwhere = tzwhere.tzwhere()

# =============================================================================
# import streamlit as st
# import streamlit.components.v1 as components
# import myfunction
# from datetime import datetime
# 
# st.header("test html import")
# 
# 
# 
# d = st.date_input(
#     "When's your birthday", min_value = datetime(1910, 1, 1), max_value = datetime(2080, 12, 31))
# st.write('Your birthday is:', d)
# 
# #print(type(d.year))
# 
# hour, minute = st.columns(2)
# 
# with hour:
#    t_hour = st.selectbox('Birth hour is:', options = range(0,24), key = 'h')
#    st.write('Birth hour is:', t_hour)
# 
# with minute:
#    t_minute = st.selectbox('Birth minute is:', options = range(0,60), key = 'm')
#    st.write('Birth minute is:', t_minute)
# 
# #components.iframe("http://127.0.0.1:5500/AstroChart/project/examples/radix/radix.html", height=700)
# #print(type(t_hour))
# 
# birth2 = datetime(d.year,d.month,d.day,t_hour,t_minute)
# #birth2 = datetime(2000, 12, 26 , 12, 0)
# info2 = ['shenzhen','china',birth2]
# 
# 
# res = myfunction.JSreadable(myfunction.getAllinfo(*info2))
# astrodata = "const data = " + str(res)
# 
# location = "chartHtml/radix.html"
# #location = "testHtml.html"
# HtmlFile = open(location, 'r', encoding='utf-8')
# source_code = HtmlFile.read() 
# 
# location2 = "chartHtml/astrochart.js"
# HtmlFile2 = open(location2, 'r', encoding='utf-8')
# astroChartFunction = HtmlFile2.read() 
# astroChartFunction = "<script>\n" + astroChartFunction + "\n</script>"
# #print(astroChartFunction)
# 
# source_code = source_code.replace('<script src="../../build/astrochart.js"></script>', astroChartFunction)
# source_code = source_code.replace('const data = [0]', astrodata)
# 
# #print(type(source_code))
# components.html(source_code, height=600)
# =============================================================================

#st.write(myfunction.JSreadable(myfunction.getAllinfo(*info2)))