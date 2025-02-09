#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd

st.title('Resultados de Enero--Comparativa entre dos Clubes')

df = pd.read_excel('resultado1.xlsx')

st.write(df)
