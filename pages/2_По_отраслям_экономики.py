import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

def real_wage_df(df1, df2, s):
    nw = pd.DataFrame(df1['год'])
    nw['data'] = df1[s]
    nw['parameter'] = ['НЗП'] * len(nw)

    rw = pd.DataFrame(df1['год'])
    rw['data'] = df1[s] / ((100 + df2['Всего'])/100)
    rw['parameter'] = ['РЗП'] * len(rw)

    return pd.concat([nw, rw], ignore_index=True)





df = pd.read_csv('data/out.csv')
df = df.drop(['всего по  экономике', 'производство пищевых продуктов, включая напитки, и табака'], axis=1)
df['год'] = pd.to_datetime(df['год'], format='%Y')
inflation = pd.read_csv('data/inflation.csv').sort_values('Год').reset_index()

sbox = tuple(df.drop(['год'], axis=1).columns)

selector = st.selectbox(
    'Выберите отрасль экономики:',
    sbox
)

st.dataframe(real_wage_df(df, inflation, selector))