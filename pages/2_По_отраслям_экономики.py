import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

def real_wage_df(df1, df2, s, param1, param2):
    nw = pd.DataFrame(df1['год'])
    nw['data'] = df1[s]
    nw['parameter'] = [param1] * len(nw)

    rw = pd.DataFrame(df1['год'])
    rw['data'] = df1[s] / ((100 + df2['Всего'])/100)
    rw['parameter'] = [param2] * len(rw)

    return pd.concat([nw, rw], ignore_index=True)

def wage_rate_df(df1, df2, s, param1, param2):
    nwr = pd.DataFrame(df1['год'].iloc[1:])
    arr = list(df1[s])
    res = []
    for i in range(1, len(arr)):
        res.append(arr[i] / arr[i-1])

    xs = np.array(res) * 100

    ys = df2['Всего'].iloc[1:]
    nwr['data'] = 100 + ys
    nwr['parameter'] = [param1] * len(nwr)

    rwr = pd.DataFrame(df1['год'].iloc[1:])
    rwr['data'] = 100*xs / nwr['data']
    rwr['parameter'] = [param2] * len(rwr)

    return pd.concat([nwr, rwr], ignore_index=True)

def to_base_year(df1, df2, param1, param2):
    cpi = df1.iloc[1:]
    lst = list(cpi['Всего'])
    res = []
    t = 1
    for i in range(len(lst)):
            t = t * ((100 + lst[i])/100)
            res.append(t)

    xs = 100 * np.array(res)

    rwr = df2.loc[df2['parameter']==param2]
    ls = list(rwr.data)
    res = []
    t = 1
    for i in range(len(ls)):
            t = t * ls[i] / 100
            res.append(t)

    ys = 100*np.array(res)

    c_rate = pd.DataFrame(df['год'].iloc[1:])
    c_rate['data'] = xs
    c_rate['parameter'] = [param1] * len(c_rate)

    r_rate = pd.DataFrame(df['год'].iloc[1:])
    r_rate['data'] = ys
    r_rate['parameter'] = [param2] * len(c_rate)
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
df = df.drop(['производство пищевых продуктов, включая напитки, и табака'], axis=1)
df['год'] = pd.to_datetime(df['год'], format='%Y')
inflation = pd.read_csv('data/inflation.csv').sort_values('Год').reset_index()

sbox = (
     'сельское хозяйство, охота и лесное хозяйство',
     'рыболовство, рыбоводство',
     'производство электрооборудования, электронного и оптического оборудования',
)

selector = st.sidebar.selectbox(
    'Выберите отрасль экономики:',
    sbox
)

nrw_df = real_wage_df(df, inflation, selector, 'НЗП', 'РЗП')
nrw_df_allover = real_wage_df(df, inflation, 'всего по  экономике', 'НЗП по экономике', 'РЗП по экономике')

wr_df = wage_rate_df(df, inflation, selector, 'ИПЦ', 'ИРЗП')
wr_df_allover = wage_rate_df(df, inflation, 'всего по  экономике', 'ИПЦ', 'ИРЗП по экономике')

cr_df = to_base_year(inflation, wr_df, 'ИПЦ', 'ИРЗП')
cr_df_allover = to_base_year(inflation, wr_df_allover, 'ИПЦ', 'ИРЗП по экономике')

tab1, tab2, tab3 = st.tabs([
    'НЗП и РЗП за 2000-2023 гг.',
    'ИПЦ и ИЗРП за 2000-2023 гг.',
    'ИПЦ и ИЗРП к базовому году'
])

if selector == 'сельское хозяйство, охота и лесное хозяйство':
     text_tab1 = """
        С 2000 года наблюдается устойчивый рост номинальных и реальных заработных плат. Уровень зарплат ниже среднего
        по экономике.
    """
     text_tab2 = """
        С 2000 по 2008 индекс реальных заработных плат выше или равен индекса потребительских цен,
        т.е. зарплаты растут быстрее чем потребительские цены. Падение реальных заработных плат в 2008-2010 гг.
        связано с экономических кризисом. Восстановление произошло в 2011 году. Следующий спад 2014 года 
        связан с геополитическими процессами и обусловлен введением санкций против отдельных отраслей экономики.
        В 2016 году происходит рост заработных плат, связанный с перестройкой отрасли после введения контрсанкций
        против недружественных стран, что привело к увеличению инвестиций в отрасль.
    """
     text_tab3 = """
        Темпы роста реальных зарплат в отрасли выше или равны темпам инфляции, после спада 2014 года. 
    """
elif selector == 'рыболовство, рыбоводство':
     text_tab1 = """
        С 2004 года наблюдается устойчивый рост номинальных и реальных заработных плат. Уровень зарплат сравним
        со средним по экономике. После 2014 года происходит резкое увеличение зарплаты по отрасли.
    """
     text_tab2 = """
        В 2003 году наблюдается провал по уровню реальной заработной платы. Падение реальных заработных плат в 2008-2010 гг.
        связано с финансово-экономическим кризисом. Восстановление произошло в 2011 году. 
        В 2014 году происходит рост заработных плат, связанный с перестройкой отрасли после введения контрсанкций
        против недружественных стран и внедрением государственных программ по обновлению флота и развитию отрасли.
    """
     text_tab3 = """
        Темпы роста реальных зарплат в отрасли выше или равны темпам инфляции, после спада 2008 года. 
    """
elif selector == 'производство электрооборудования, электронного и оптического оборудования':
    text_tab1 = """
        С 2000 года наблюдается устойчивый рост номинальных и реальных заработных плат. В последние годы рост реальных заработных плат меньше роста реальных, что связано с более высоким уровнем инфляции.
    """
    text_tab2 = """
       Согласно графику, с 2000 по 2008 кривая индекса реальных заработных плат выше или  соответствует кривой индекса потребительских цен, т.е. зарплаты  росли быстрее чем  цены на потребительские товары. Финансово-экономический кризис 2008-2010 гг. привел к падению уровня реальных заработных плат.  Восстановление произошло в 2010 году. Следующий спад 2014 года связан с геополитическими процессами и обусловлен введением санкций против отдельных отраслей экономики. В 2016 году происходит восстановление экономики. В 2020 году происходит следующий спад, связанный с пандемией COVID-19, которая усугубилась геополитическими факторами и введением новых пакетов санкций.
    """
    text_tab3 = """
        Темпы роста реальных зарплат в отрасли после 2014 года ниже темпов инфляции, но выше среднего по экономике.
    """

allover_on = st.sidebar.toggle(
     "Отображать данные по всей экономике"
)
if allover_on:
    with tab1:
        nrw = plot_chart(nrw_df, 'Заработная плата, руб.')
        nrw_allover = plot_chart(nrw_df_allover, 'Заработная плата, руб.')
        st.altair_chart(nrw+nrw_allover, use_container_width=True, theme='streamlit')
        st.markdown(text_tab1)
        

    with tab2:
        wr = plot_chart(wr_df, '% к предыдущему году году')
        wr_allover = plot_chart(wr_df_allover[wr_df_allover['parameter']=='ИРЗП по экономике'], '% к предыдущему году году')
        st.altair_chart(wr+wr_allover, use_container_width=True, theme='streamlit')
        st.markdown(text_tab2)
       

    with tab3:
        cr_rate = plot_chart(cr_df, '% к базовому году')
        cr_rate_allover = plot_chart(cr_df_allover[cr_df_allover['parameter']=='ИРЗП по экономике'], '% к предыдущему году году')
        st.altair_chart(cr_rate+cr_rate_allover, use_container_width=True, theme='streamlit')
        st.markdown(text_tab3)
else:
    with tab1:
        nrw = plot_chart(nrw_df, 'Заработная плата, руб.')
        st.altair_chart(nrw, use_container_width=True, theme='streamlit')
        st.markdown(text_tab1)

    with tab2:
        wr = plot_chart(wr_df, '% к предыдущему году году')
        st.altair_chart(wr, use_container_width=True, theme='streamlit')
        st.markdown(text_tab2)

    with tab3:
        cr_rate = plot_chart(cr_df, '% к базовому году')
        st.altair_chart(cr_rate, use_container_width=True, theme='streamlit')
        st.markdown(text_tab3)
