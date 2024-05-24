import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

dian = pd.read_csv('datos_recaudo_const.csv')
an = dian['Año']
dian_porc = dian.div(dian['Total'], axis=0)
dian_porc['Año'] = an

aggs = {'ACTIVIDAD INTERNA': ['Renta y complementarios /1', 'Renta cuotas',
       'Retención en la fuente a título de renta /2', 'IVA_IN',
       'Declaraciones IVA', 'Retención en la fuente a título de IVA',
       'Timbre nacional', 'G.M.F.', 'Patrimonio /3', 'Riqueza /4',
       'Impuesto al consumo /5', 'Impuesto gasolina y ACPM',
       'Impuesto al carbono /6', 'CREE', 'Declaraciones CREE /7',
       'Retención CREE', 'Impuesto unificado RST (Simple)  /8',
       'Impuesto de normalización tributaria /9',
       'Consumo bienes inmuebles /10',
       'Productos plásticos de un solo uso /11',
       'Impuestos saludables - Bebidas azucaradas /12',
       'Impuestos saludables - Comestibles ultraprocesados /13'],
        'ACTIVIDAD EXTERNA': ['IVA_EX', 'Arancel /14'],
        'TOTAL': ['Renta y complementarios /1', 'Renta cuotas',
       'Retención en la fuente a título de renta /2', 'IVA_IN',
       'Declaraciones IVA', 'Retención en la fuente a título de IVA',
       'Timbre nacional', 'G.M.F.', 'Patrimonio /3', 'Riqueza /4',
       'Impuesto al consumo /5', 'Impuesto gasolina y ACPM',
       'Impuesto al carbono /6', 'CREE', 'Declaraciones CREE /7',
       'Retención CREE', 'Impuesto unificado RST (Simple)  /8',
       'Impuesto de normalización tributaria /9',
       'Consumo bienes inmuebles /10',
       'Productos plásticos de un solo uso /11',
       'Impuestos saludables - Bebidas azucaradas /12',
       'Impuestos saludables - Comestibles ultraprocesados /13', 'IVA_EX', 'Arancel /14']}

st.title("Repo - taxes")

st.divider()

agg = st.selectbox("Seleccione un agregado", ['ACTIVIDAD INTERNA',
                                              'ACTIVIDAD EXTERNA',
                                              'TOTAL'])

filtro = dian[aggs[agg]]

if agg == 'TOTAL':
    sumar_iva = st.checkbox("Sumar IVA")
    if sumar_iva:
        filtro['IVA_T'] = filtro['IVA_IN'] + filtro['IVA_EX']
        dian['IVA_T'] = dian['IVA_IN'] + dian['IVA_EX']
        dian_porc['IVA_T'] = dian['IVA_T'] / dian['Total']

comp_taxes = st.multiselect("Seleccione uno o varios impuestos: ", filtro.columns)

filtro2 = filtro[comp_taxes]

if len(comp_taxes) == 0:
    st.warning("Seleccione variables para graficar")
    st.stop()

fig, ax = plt.subplots(2, 1, figsize=(14, 6))

filtro2['Año'] = dian['Año']
filtro2 = filtro2.set_index('Año')

filtro2.plot(kind='line', ax=ax[0])
ax[1].set_ylim(0, 1.1)
ax[1].axhline(1, color='black', alpha=0.2, ls='--')
dian_porc.set_index('Año')[comp_taxes].plot(kind='bar', stacked=True, ax=ax[1])


st.pyplot(fig)


