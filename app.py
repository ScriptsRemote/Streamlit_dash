##importar as bibliotecas 
import streamlit as st 
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go

##Abrir no csv
df = pd.read_csv(r'asset\NDVI__Precipitation__and_Temperature_Data.csv')

##Converter a primeira para
df['Date']= pd.to_datetime(df['Date'])

df['Year-Month']= df['Date'].dt.to_period('M')

##Agregar dados 
df_monthly = df.groupby('Year-Month').agg({
    'Precipitation (mm)':'sum',
    'Temperature (°C)':'mean',
    'NDVI': 'mean'  
    
}).reset_index()

##Gerar nosso
ndvi_trace = go.Scatter(x=df_monthly['Year-Month'].astype(str),
                        y=df_monthly['NDVI'],
                        mode='lines',
                        name='NDVI',
                        line=dict(color='green'))

precipitation_trace = go.Bar(x=df_monthly['Year-Month'].astype(str),
                        y=df_monthly['Precipitation (mm)'],
                        name='Precipitação',
                        yaxis='y2',
                        opacity=0.6,
                        marker=dict(color='blue'))


layout =go.Layout(
    title='NDVI e Precipitação Mensal',
    xaxis=dict(title='Mês'),
    yaxis=dict(title='NDVI', range=[0,1]),
    yaxis2=dict(title='Precipitação', overlaying='y', side='right'),
    legend=dict(x=0, y=1.1, orientation='h'),
    barmode='overlay'
    
)

fig1 = go.Figure(data=[ndvi_trace,precipitation_trace], layout=layout)

###Definir a figura 2 
# Gráfico de heatmap para Temperatura
heatmap_data = df_monthly.pivot_table(index=df_monthly['Year-Month'].dt.year, columns=df_monthly['Year-Month'].dt.month, values='Temperature (°C)')

fig2= px.imshow(
    heatmap_data,
    labels=dict(x= 'Month',y ='Year', color='Temperature (°C)'),
    x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    title="Temperature Heatmap Over 24 Months",
    color_continuous_scale="RdYlGn"
)

##Set configuração da pagina
st.set_page_config(layout='wide',
                   initial_sidebar_state='expanded')

st.sidebar.write('App criado para apresentação dos resultados de NDVI, Precipitação e Temperatura da Fazenda Youtube')
st.sidebar.image(r'asset\ndvi.png')

##Criar um titulo
st.title('NDVI, Precipitação e Temperatura Dashboard')

st.dataframe(df_monthly, width=1200, height=400)

##Colunas 
col1, col2 = st.columns([0.5,0.5])

with col1:
    st.subheader('NDVI e Precipitação')
    st.plotly_chart(fig1)
    
with col2:
    st.subheader('Temperatura')
    st.plotly_chart(fig2)

