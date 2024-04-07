import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

def calculate_wi(df, s):
    arr = list(df[s])
    res = []
    res.append(2223 / 1523 * 100)
    for i in range(1, len(arr)):
        res.append(arr[i] / arr[i-1] * 100)
    
    return np.array(res)

def cpi_rate(df, s):
    arr = list(df[s])
    res = []
    t = 1
    for i in range(len(arr)):
        t = t * ((100 + arr[i])/100)
        res.append(t)
    return np.array(res)*100


def rwi_rate(df, s):
    arr = list(df[s])
    res = []
    t = 1
    for i in range(len(arr)):
        t = t * arr[i]/100
        res.append(t)
    return np.array(res)*100

sheet_1 = pd.read_csv('data/sheet_1.csv')
sheet_2 = pd.read_csv('data/sheet_2.csv').rename(columns={'Всего': 'Всего по  экономике'})
inflation = pd.read_csv('data/inflation.csv').sort_values('Год').reset_index()


nominal_wage = pd.concat([sheet_1[['Год', 'Всего по  экономике']], sheet_2[['Год', 'Всего по  экономике']]], ignore_index=True)
nominal_wage['Год'] = pd.to_datetime(nominal_wage['Год'], format='%Y')
nominal_wage['parameter'] = ['НЗП'] * len(nominal_wage)

real_wage = pd.DataFrame( nominal_wage['Год'])
real_wage['Всего по  экономике'] = nominal_wage['Всего по  экономике'] / ((100 + inflation['Всего']) / 100)
real_wage['parameter'] = ['РЗП'] * len(nominal_wage)
nrw_dat = pd.concat([nominal_wage, real_wage], ignore_index=True)

nwi = pd.DataFrame(nominal_wage['Год'])
s = 'Всего по  экономике'
nwi['Всего по  экономике'] = calculate_wi(nominal_wage, s)
nwi['parameter'] = ['ИНЗП'] * len(nwi)

rwi = pd.DataFrame(nominal_wage['Год'])
s = 'Всего по  экономике'
rwi['Всего по  экономике'] = 100 * nwi['Всего по  экономике'] / ((100 + inflation['Всего']))
rwi['parameter'] = ['ИРЗП'] * len(nwi)

cpi = pd.DataFrame(nominal_wage['Год'])
cpi['Всего по  экономике'] = (100 + inflation['Всего'])
cpi['parameter'] = ['ИПЦ'] * len(nwi)
nrwi_dat = pd.concat([rwi, cpi], ignore_index=True)

cpir = pd.DataFrame(nominal_wage['Год'])
cpir['Всего по  экономике'] = cpi_rate(inflation, 'Всего')
cpir['parameter'] = ['ИПЦ к базовому году'] * len(cpir)

rwir = pd.DataFrame(nominal_wage['Год'])
rwir['Всего по  экономике'] = rwi_rate(rwi, 'Всего по  экономике')
rwir['parameter'] = ['ИРЗП к базовому году'] * len(cpir)
cri_rate = pd.concat([cpir, rwir], ignore_index=True)

base_1 = alt.Chart(nrw_dat).encode(
    alt.Color('parameter'),
    alt.X(
        'Год',
        axis = alt.Axis(title='год'))
)

base_2 = alt.Chart(nrwi_dat).encode(
    alt.Color('parameter'),
    alt.X(
        'Год',
        axis = alt.Axis(title='год'))
)
base_3 = alt.Chart(cri_rate).encode(
    alt.Color('parameter'),
    alt.X(
        'Год',
        axis = alt.Axis(title='год'))
)
tab1, tab2, tab3 = st.tabs([
    'НЗП и РЗП за 2000-2023 гг.',
    'ИПЦ и ИЗРП за 2000-2023 гг.',
    'ИПЦ и ИЗРП к базовому году'
])

nrw = base_1.mark_line(
    point=alt.OverlayMarkDef(filled=False, fill="white")
).encode(
    alt.Y('Всего по  экономике', title='Заработная плата, руб.')
)

nrwi = base_2.mark_line(
        point=alt.OverlayMarkDef(filled=False, fill="white")
).encode(
    alt.Y('Всего по  экономике', title='% к предыдущему году')
)
cri_rate_chart = base_3.mark_line(
        point=alt.OverlayMarkDef(filled=False, fill="white")
).encode(
    alt.Y('Всего по  экономике', title='% к базовому году')
)

with tab1: 
    st.altair_chart(nrw, use_container_width=True)
    st.markdown(
        """
        С 2000 года наблюдается устойчивый рост номинальных и реальных заработных плат.
"""
    )

with tab2:  
    st.altair_chart(nrwi, use_container_width=True)
    st.markdown(
        """
        С 2000 по 2008 индекс реальных заработных плат выше или равен индекса потребительских цен,
        т.е. зарплаты растут быстрее чем потребительские цены. Падение реальных заработных плат в 2008-2010 гг.
        связано с экономических кризисом. Восстановление произошло в 2010 году. Следующий спад 2014 года 
        связан с геополитическими процессами и обусловлен введением санкций против отдельных отраслей экономики.
        В 2016 году происходит восстановление экономики. В 2020 году происходит следующий спад связанный с 
        пандемией COVID-19, которая усугубилась геополитическими факторами и введением новых пакетов санкций.
""")

with tab3:
    st.altair_chart(cri_rate_chart, use_container_width=True, theme='streamlit')
    st.markdown(
        """
        С 2014 года наблюдается замедление роста индекса реальных заработных плат, связанное с введением
        санкций и спадом мировой экономики из-за пандемии COVID-19. Начало СВО привело к обрыву производственных
        и торговых цепочек, что привело к увеличению потребительских цен.

"""
)
