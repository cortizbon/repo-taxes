import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

DIC_COLORES = {'verde':["#009966"],
               'ro_am_na':["#FFE9C5", "#F7B261","#D8841C", "#dd722a","#C24C31", "#BC3B26"],
               'az_verd': ["#CBECEF", "#81D3CD", "#0FB7B3", "#009999"],
               'ax_viol': ["#D9D9ED", "#2F399B", "#1A1F63", "#262947"],
               'ofiscal': ["#F9F9F9", "#2635bf"]}



st.set_page_config(layout="wide")

st.title("Histórico de impuestos")

df = pd.read_csv('datasets/recaudo.csv')
df['Valor (Constantes - 18)'] = (df['Valor (Constantes - 18)'] / 1_000).round(1)



tab1, tab2 = st.tabs(['General', 'Detalle interno'])

with tab1:

    piv_year = df.groupby(['Año'])['Valor (Constantes - 18)'].sum().reset_index()
    acum = (piv_year
                                            .groupby(['Año'])['Valor (Constantes - 18)']
                                            .sum()
                                            .reset_index())
    fig = make_subplots(rows=1, cols=2, x_title='Año',  )
            
    fig.add_trace(
                    go.Scatter(
                    x=acum['Año'],  # x-axis for forecasted values
                    y=acum['Valor (Constantes - 18)'],     # The forecasted values
                    mode='lines+markers',          # Just lines (no markers here)
                    name='Recaudo', showlegend=True,
                    line=dict(color=DIC_COLORES['ax_viol'][1], width=2, dash='dash'),
                    marker=dict(color=DIC_COLORES['ax_viol'][1], size=8),  # Dashed line for forecast
                ), row=1, col=1
                )

    piv_recaudo = (df
                            .groupby(['Año', 'Agregación'])['Valor (Constantes - 18)']
                            .sum()
                            .reset_index())
    piv_recaudo['total'] = piv_recaudo.groupby(['Año'])['Valor (Constantes - 18)'].transform('sum')

    piv_recaudo['%'] = ((piv_recaudo['Valor (Constantes - 18)'] / piv_recaudo['total']) * 100).round(2)
    dict_rec = {'Actividad interna':DIC_COLORES['az_verd'][2],
                'Actividad externa':DIC_COLORES['ax_viol'][1],
                'Por clasificar':DIC_COLORES['ro_am_na'][3]}

    for i, group in piv_recaudo.groupby('Agregación'):
        fig.add_trace(go.Bar(
                    x=group['Año'],
                    y=group['%'],
                    name=i, marker_color=dict_rec[i],
                ),  row=1, col=2)


    fig.update_layout(barmode='stack', hovermode='x unified')
    fig.update_layout(width=1000, height=500, legend=dict(orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1), title='Histórico general <br><sup>Cifras en miles de millones de pesos</sup>', yaxis_tickformat='.0f')


    st.plotly_chart(fig)  

    rec_int = df[df['Agregación'] == 'Actividad interna']
    piv_recaudo = (rec_int
                                .groupby(['Año', 'Impuesto_alt'])['Valor (Constantes - 18)']
                                .sum()
                                .reset_index())
    acum = (piv_recaudo
                                            .groupby(['Año'])['Valor (Constantes - 18)']
                                            .sum()
                                            .reset_index())
    piv_recaudo['total'] = piv_recaudo.groupby(['Año'])['Valor (Constantes - 18)'].transform('sum')

    piv_recaudo['%'] = ((piv_recaudo['Valor (Constantes - 18)'] / piv_recaudo['total']) * 100).round(2)
    fig = make_subplots(rows=1, cols=2, x_title='Año',  )


            
    fig.add_trace(
                    go.Scatter(
                    x=acum['Año'],  # x-axis for forecasted values
                    y=acum['Valor (Constantes - 18)'],     # The forecasted values
                    mode='lines+markers',          # Just lines (no markers here)
                    name='Recaudo de impuestos de actividad interna', showlegend=True,
                    line=dict(color=DIC_COLORES['ax_viol'][1], width=2, dash='dash'),
                    marker=dict(color=DIC_COLORES['ax_viol'][1], size=8),  # Dashed line for forecast
                ), row=1, col=1
                )
    dict_alt = {'IVA':DIC_COLORES['az_verd'][2],
                'Renta':DIC_COLORES['ax_viol'][1],
                'Otros':DIC_COLORES['ro_am_na'][3]}

    for i, group in piv_recaudo.groupby('Impuesto_alt'):
                    fig.add_trace(go.Bar(
                        x=group['Año'],
                        y=group['%'],
                        name=i, marker_color=dict_alt[i]
                    ),  row=1, col=2)


    fig.update_layout(barmode='stack', hovermode='x unified')
    fig.update_layout(width=1000, height=500, legend=dict(orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1), title='Histórico interno <br><sup>Cifras en miles de millones de pesos</sup>', yaxis_tickformat='.0f')


    st.plotly_chart(fig)

    rec_ext = df[df['Agregación'] == 'Actividad externa']
    piv_recaudo = (rec_ext
                                .groupby(['Año', 'Impuesto específico'])['Valor (Constantes - 18)']
                                .sum()
                                .reset_index())
    acum = (piv_recaudo
                                            .groupby(['Año'])['Valor (Constantes - 18)']
                                            .sum()
                                            .reset_index())
    piv_recaudo['total'] = piv_recaudo.groupby(['Año'])['Valor (Constantes - 18)'].transform('sum')

    piv_recaudo['%'] = ((piv_recaudo['Valor (Constantes - 18)'] / piv_recaudo['total']) * 100).round(2)
    fig = make_subplots(rows=1, cols=2, x_title='Año',  )
            
    fig.add_trace(
                    go.Scatter(
                    x=acum['Año'],  # x-axis for forecasted values
                    y=acum['Valor (Constantes - 18)'],     # The forecasted values
                    mode='lines+markers',          # Just lines (no markers here)
                    name='Recaudo acumulado', showlegend=True,
                    line=dict(color=DIC_COLORES['ax_viol'][1], width=2, dash='dash'),
                    marker=dict(color=DIC_COLORES['ax_viol'][1], size=8),  # Dashed line for forecast
                ), row=1, col=1
                )
    dict_alt = {'IVA_ext':DIC_COLORES['ro_am_na'][3],
                'Arancel':DIC_COLORES['az_verd'][2]}
    for i, group in piv_recaudo.groupby('Impuesto específico'):
                    fig.add_trace(go.Bar(
                        x=group['Año'],
                        y=group['%'],
                        name=i, marker_color=dict_alt[i]
                    ),  row=1, col=2)


    fig.update_layout(barmode='stack', hovermode='x unified')
    fig.update_layout(width=1000, height=500, legend=dict(orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1), title='Histórico externo <br><sup>Cifras en miles de millones de pesos</sup>', yaxis_tickformat='.0f')


    st.plotly_chart(fig)

with tab2:

    rec_int = df[df['Agregación'] == 'Actividad interna']
    piv_recaudo = (rec_int
                                .groupby(['Año', 'Impuesto específico'])['Valor (Constantes - 18)']
                                .sum()
                                .reset_index())
    acum = (piv_recaudo
                                            .groupby(['Año'])['Valor (Constantes - 18)']
                                            .sum()
                                            .reset_index())
    piv_recaudo['total'] = piv_recaudo.groupby(['Año'])['Valor (Constantes - 18)'].transform('sum')

    piv_recaudo['%'] = ((piv_recaudo['Valor (Constantes - 18)'] / piv_recaudo['total']) * 100).round(2)
    fig = make_subplots(rows=1, cols=2, x_title='Año',  )
            
    fig.add_trace(
                    go.Scatter(
                    x=acum['Año'],  # x-axis for forecasted values
                    y=acum['Valor (Constantes - 18)'],     # The forecasted values
                    mode='lines+markers',          # Just lines (no markers here)
                    name='Recaudo acumulado', showlegend=True,
                    line=dict(color=DIC_COLORES['ax_viol'][1], width=2, dash='dash'),
                    marker=dict(color=DIC_COLORES['ax_viol'][1], size=8),  # Dashed line for forecast
                ), row=1, col=1
                )
    dict_alt = {'IVA':DIC_COLORES['az_verd'][2],
                'Renta':DIC_COLORES['ax_viol'][1]}
    for i, group in piv_recaudo.groupby('Impuesto específico'):
        if i in ['Renta', 'IVA']:
                    fig.add_trace(go.Bar(
                        x=group['Año'],
                        y=group['%'],
                        name=i, marker_color=dict_alt[i]
                    ),  row=1, col=2)
        else:
            fig.add_trace(go.Bar(
                        x=group['Año'],
                        y=group['%'],
                        name=i
                    ),  row=1, col=2)



    fig.update_layout(barmode='stack', hovermode='x unified')
    fig.update_layout(width=1000, height=500, showlegend=False, title='Histórico interno <br><sup>Cifras en miles de millones de pesos</sup>', yaxis_tickformat='.0f')


    st.plotly_chart(fig)

    year = st.select_slider("Seleccione un año", rec_int['Año'].unique().tolist())

    rec_int = rec_int[rec_int['Año'] == year]
    fig = px.treemap(rec_int, path=[px.Constant("Recaudo interno"), "Impuesto"], values='Valor (Constantes - 18)')
    fig.update_layout(width=1000, height=500, showlegend=False, title='Matriz de composición del recaudo interno<br><sup>Cifras en miles de millones de pesos</sup>', yaxis_tickformat='.0f')


    st.plotly_chart(fig)