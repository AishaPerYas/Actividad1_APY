import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("../../../data/final/datos_finales.csv", sep=";")

st.set_page_config(
    page_title="Herramienta de Visualización de Datos - 13MBID",
    page_icon="📊",
    layout="wide",
)

# Título de la aplicación
st.title("Herramienta de Visualización de Datos - 13MBID")
st.write(
    "Esta aplicación permite explorar y visualizar los datos del proyecto en curso."
)
st.write("Desarrollado por: Aisha Pervaz Yasmeen")
st.markdown('---')

# Gráficos
st.header("Gráficos")
st.subheader("Caracterización de los créditos otorgados:")

# Cantidad de créditos por objetivo del mismo

creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

#Visualización

st.plotly_chart(creditos_x_objetivo, use_container_width=True)

# Histograma de los importes de créditos otorgados

histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')

st.plotly_chart(histograma_importes, use_container_width=True)

# Conteo de ocurrencias por estado
estado_credito_counts = df['estado_credito_N'].value_counts()

# Gráfico de torta de estos valores
fig = go.Figure(data=[go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts)])
fig.update_layout(title_text='Distribución de créditos por estado registrado')

st.plotly_chart(fig, use_container_width=True)


# Se agrega un selector para el tipo de crédito y se aplica a los gráficos siguientes:

tipo_credito = st.selectbox(
    "Selecciona el tipo de crédito",
    df['objetivo_credito'].unique(),
)

st.write("Tipo de crédito seleecionado: ", tipo_credito)

df_filtrado = df[df['objetivo_credito'] == tipo_credito]

col1, col2 = st.columns(2)
with col1:
    # Gráfico de barras apiladas: Comparar la distribución de créditos por estado y objetivo
    barras_apiladas = px.histogram(df_filtrado, x='objetivo_credito', color='estado_credito_N', 
                                title='Distribución de créditos por estado y objetivo',
                                barmode='stack')
    barras_apiladas.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

    st.plotly_chart(barras_apiladas, use_container_width=True)

with col2: 
    # Conteo de ocurrencias por caso
    falta_pago_counts = df_filtrado['falta_pago'].value_counts()

    # Create a Pie chart
    fig = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
    fig.update_layout(title_text='Distribución de créditos en función de registro de mora')

    st.plotly_chart(fig, use_container_width=True)



# Definir el orden personalizado
orden_antiguedad = ['menor_2y', '2y_a_4y', 'mayor_4y']

# Ordenar los datos según el orden personalizado
df_ordenado = df.groupby('antiguedad_cliente')['importe_solicitado'].mean().reset_index()
df_ordenado['antiguedad_cliente'] = pd.Categorical(df_ordenado['antiguedad_cliente'], categories=orden_antiguedad, ordered=True)
df_ordenado = df_ordenado.sort_values('antiguedad_cliente')

# Crear el gráfico de líneas
lineas_importes_antiguedad = px.line(df_ordenado, x='antiguedad_cliente', y='importe_solicitado',
                                     title='Evolución de los importes solicitados por antigüedad del cliente')
lineas_importes_antiguedad.update_layout(xaxis_title='Antigüedad del cliente', yaxis_title='Importe solicitado promedio')


st.plotly_chart(lineas_importes_antiguedad, use_container_width=True)

# Gráfico de cajas por objetivo del crédito
box_importes_objetivo = px.box(
    df,
    x='objetivo_credito',
    y='importe_solicitado',
    title='Distribución de los importes solicitados por objetivo del crédito',
    points='all',  # Para mostrar todos los puntos individuales también
    color='objetivo_credito'  # Diferenciar colores por categoría
)

# Ajustar etiquetas
box_importes_objetivo.update_layout(
    xaxis_title='Objetivo del crédito',
    yaxis_title='Importe solicitado',
    showlegend=False 
)

st.plotly_chart(box_importes_objetivo, use_container_width=True)

# Gráfico de dispersión
scatter_importe_duracion = px.scatter(
    df,
    x='duracion_credito',
    y='importe_solicitado',
    color='estado_credito_N',  # Colorea por estado del crédito
    title='Relación entre Importe Solicitado y Duración del Crédito, según Estado del Crédito',
    labels={
        'duracion_credito': 'Duración del crédito (meses)',
        'importe_solicitado': 'Importe solicitado',
        'estado_credito_N': 'Estado del crédito'
    }
)

scatter_importe_duracion.update_traces(marker=dict(size=8, opacity=0.7))
scatter_importe_duracion.update_layout(
    xaxis_title='Duración del crédito (meses)',
    yaxis_title='Importe solicitado',
)

st.plotly_chart(scatter_importe_duracion, use_container_width=True)

# Seleccionamos las columnas numéricas que queremos analizar
variables_correlacion = df[['importe_solicitado', 'duracion_credito', 'personas_a_cargo']]

# Calculamos la matriz de correlación
matriz_correlacion = variables_correlacion.corr()

# Creamos el heatmap
heatmap_correlacion = px.imshow(
    matriz_correlacion,
    text_auto=True,  # Muestra los valores dentro de cada celda
    color_continuous_scale='RdBu_r',
    title='Mapa de calor de correlación entre variables'
)

heatmap_correlacion.update_layout(
    xaxis_title='Variables',
    yaxis_title='Variables'
)

st.plotly_chart(heatmap_correlacion, use_container_width=True)