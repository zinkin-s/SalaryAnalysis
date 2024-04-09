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

    xs = np.array(res) * 100

    ys = df2['Всего'].iloc[1:]
    nwr['data'] = 100 + ys
    nwr['parameter'] = ['ИПЦ'] * len(nwr)

    rwr = pd.DataFrame(df1['год'].iloc[1:])
    rwr['data'] = 100*xs / nwr['data']
    rwr['parameter'] = ['ИРЗП'] * len(rwr)

    return pd.concat([nwr, rwr], ignore_index=True)

def to_base_year(df1, df2):
    cpi = df1.iloc[1:]
    lst = list(cpi['Всего'])
    res = []
    t = 1
    for i in range(len(lst)):
            t = t * ((100 + lst[i])/100)
            res.append(t)

    xs = 100 * np.array(res)

    rwr = df2.loc[df2['parameter']=='ИРЗП']
    ls = list(rwr.data)
    res = []
    t = 1
    for i in range(len(ls)):
            t = t * ls[i] / 100
            res.append(t)

    ys = 100*np.array(res)

    c_rate = pd.DataFrame(df['год'].iloc[1:])
    c_rate['data'] = xs
    c_rate['parameter'] = ['ИПЦ'] * len(c_rate)

    r_rate = pd.DataFrame(df['год'].iloc[1:])
    r_rate['data'] = ys
    r_rate['parameter'] = ['ИРЗП'] * len(c_rate)
    return pd.concat([c_rate, r_rate], ignore_index=True)

def plot_chart(df, title):
    base = alt.Chart(df).encode(
    alt.Color('parameter'),
    alt.X(
        'год',
        axis = alt.Axis(title='год')))

    chart = base.mark_line(
    point=alt.OverlayMarkDef(filled=False, fill="white")
    ).encode(
    alt.Y('data', title=title))
    return chart


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

wr_df = wage_rate_df(df, inflation, selector)

cr_df = to_base_year(inflation, wr_df)

tab1, tab2, tab3 = st.tabs([
    'НЗП и РЗП за 2000-2023 гг.',
    'ИПЦ и ИЗРП за 2000-2023 гг.',
    'ИПЦ и ИЗРП к базовому году'
])

with tab1:
    nrw = plot_chart(nrw_df, 'Заработная плата, руб.')
    st.altair_chart(nrw, use_container_width=True, theme='streamlit')

with tab2:
    wr = plot_chart(wr_df, '% к предыдущему году году')
    st.altair_chart(wr, use_container_width=True, theme='streamlit')

with tab3:
    cr_rate = plot_chart(cr_df, '% к базовому году')
    st.altair_chart(cr_rate, use_container_width=True, theme='streamlit')

chart = plot_chart(nrw_df, 'Заработная плата, руб.')
#st.altair_chart(chart, use_container_width=True, theme='streamlit')