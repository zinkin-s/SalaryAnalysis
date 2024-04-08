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

def wage_rate_df(df1, df2, s):
    nwr = pd.DataFrame(df1['год'].iloc[1:])
    arr = list(df1[s])
    res = []
    for i in range(1, len(arr)):
        res.append(arr[i] / arr[i-1])

    nwr['data'] = np.array(res) * 100
    nwr['parameter'] = ['ИНЗП'] * len(nwr)

    rwr = pd.DataFrame(df1['год'].iloc[1:])
    rwr['data'] = nwr['data'] / ((100 + df2['Всего'])/100)
    rwr['parameter'] = ['РЗП'] * len(rwr)

    return pd.concat([nwr, rwr], ignore_index=True)


df = pd.read_csv('data/out.csv')
df = df.drop(['всего по  экономике', 'производство пищевых продуктов, включая напитки, и табака'], axis=1)
df['год'] = pd.to_datetime(df['год'], format='%Y')
inflation = pd.read_csv('data/inflation.csv').sort_values('Год').reset_index()

sbox = tuple(df.drop(['год'], axis=1).columns)

selector = st.sidebar.selectbox(
    'Выберите отрасль экономики:',
    sbox
)

nrw_df = real_wage_df(df, inflation, selector)
base_1 = alt.Chart(nrw_df).encode(
    alt.Color('parameter'),
    alt.X(
        'год',
        axis = alt.Axis(title='год'))
)

nrw = base_1.mark_line(
    point=alt.OverlayMarkDef(filled=False, fill="white")
).encode(
    alt.Y('data', title='Заработная плата, руб.')
)

st.altair_chart(nrw, use_container_width=True, theme='streamlit')

st.dataframe(wage_rate_df(df, inflation, selector))
