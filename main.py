import streamlit as st
import warnings
warnings.filterwarnings("ignore")

st.write("""
  # Covid 19 Chile analytics
  #### by @zzznavarrete
""")


############# SCRAPPING #############
import urllib.request, json
import pandas as pd

API_PATH = 'https://api.github.com/repos/MinCiencia/Datos-COVID19/git/trees/master?recursive=1'

with urllib.request.urlopen(API_PATH) as url:
    tree = json.loads(url.read().decode())


# all data from json in dict format
tree = tree['tree']

### Obtiene la lista de todos los CSV de un producto en particular
def get_list_csv(product_number):
  return [x['path'] for x in tree if f"output/producto{product_number}/" in x['path'] and x['path'][-3:] == "csv"]


### Obtiene la data del CSV y extrae
def get_csv_data(raw_path):
  url_path = f"https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/{raw_path}"
  return raw_path[:-4].split("/")[2][:10] , pd.read_csv(url_path, index_col=0)


# Descomprime la lista entera de datasets historicos y les appendea la columna Fecha como indice
def extract_csv_data(product_dataset_list : list):
  # Getting datasets from each link
  data_list = pd.DataFrame
  i = 0

  for link in product_dataset_list:
    date, data = get_csv_data(link)
    #data['Fecha'] = date
    data.insert(0, "Fecha", date)
    if (i == 0):
      data_list = data
    else:
      data_list = data_list.append(data)
    i = i + 1
  
  return data_list


producto5_csvs = get_list_csv(5)
_, df_producto5  = get_csv_data(producto5_csvs[1])
df_producto5.index = pd.to_datetime(df_producto5.index)

############# END OF SCRAPPING #############


df = df_producto5.copy()
df_casos_totales = df.iloc[1:, 1:2]

st.write(""" ## `""" + str(df.index[len(df.index) - 1])[0:10] + """ ` """)



#col1, col2 = st.columns([8,2])
#col1.line_chart(df_casos_totales)
#col2.metric("Casos registrados al día: ", "70 °F", "1.2 °F")
#col1, col2 = st.columns(2)
#col1.line_chart(df['Fallecidos'])
#col2.metric("Fallecidos recuperados al día: ", "9 mph", "-8%")

import locale
locale.setlocale(locale.LC_ALL, 'es_ES')



st.title("Casos activos nacionales")
col1, col2, col3 = st.columns(3)
index_max = df_producto5['Casos activos'].argmax()
fecha_max = df_producto5.index[index_max]
max = df_producto5.iloc[index_max, 4]
current = df_producto5['Casos activos'][len(df_producto5['Casos activos'])-1]
mean_last_15d = int(df['Casos activos'].tail(15).sum() / 15)
delta = ((current/mean_last_15d)*100)-100
col1.metric("Mayor registro",locale.format('%d',  max , grouping=True, monetary=True), str(fecha_max)[0:10], delta_color="off")
col2.metric("Casos totales actuales",locale.format('%d',  current, grouping=True, monetary=True))
col3.metric("Delta respecto últ. 15 días ", str(delta)[0:3]+"%")
st.line_chart(df_producto5['Casos activos'])




st.title("Casos nuevos nacionales")
col1, col2, col3 = st.columns(3)
index_max = df_producto5['Casos nuevos totales'].argmax()
fecha_max = df_producto5.index[index_max]
max = df_producto5.iloc[index_max, 6]
current = df_producto5['Casos nuevos totales'][len(df_producto5['Casos nuevos totales'])-1]
mean_last_15d = int(df['Casos nuevos totales'].tail(15).sum() / 15)
delta = ((current/mean_last_15d)*100)-100
col1.metric("Mayor registro",locale.format('%d', max, grouping=True, monetary=True),  str(fecha_max)[0:10], delta_color="off")
col2.metric("Casos nuevos actuales ", locale.format('%d',  current, grouping=True, monetary=True))
col3.metric("Delta respecto últ. 15 días ", str(delta)[0:3]+"%")
st.line_chart(df_producto5['Casos nuevos totales'])


### DATASETS INTERESANTES:
# DP46 Curva activos vs recuperados -> https://github.com/MinCiencia/Datos-COVID19/blob/master/output/producto46/activos_vs_recuperados.csv
st.title("Curva activos vs recuperados")
p46 = get_list_csv(46)
_, df  = get_csv_data(p46[0])
df.index = pd.to_datetime(df.index)

st.line_chart(df)

# DP1 Totales por comuna incremental -> https://github.com/MinCiencia/Datos-COVID19/blob/master/output/producto1/Covid-19.csv

st.title("Casos confirmados acumulados por comuna de Santiago")
p2 = get_list_csv(2)
_, df  = get_csv_data(p2[len(p2)-1])
#import ipdb; ipdb.set_trace()
lista_comunas = ['Puente Alto', 'La Florida', 'Melipilla', 'Las Condes', 'Providencia','Maipu']
df_p = df.loc[df.Comuna.isin(lista_comunas)]
df_p = df_p.tail(len(lista_comunas))
df_p = df_p.reset_index().set_index('Comuna')
df_p = df_p.sort_values('Poblacion')

chart_data = pd.concat([df_p['Casos Confirmados'], df_p['Poblacion']], axis=1)

st.bar_chart(chart_data)

# DP4 - Casos totales por región: Descripción -> https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto4
# DP76 - Avance en Campaña de Vacunación COVID-19 -> https://github.com/MinCiencia/Datos-COVID19/blob/master/output/producto76/vacunacion_t.csv | https://github.com/MinCiencia/Datos-COVID19/blob/master/output/producto76/grupo_t.csv | https://github.com/MinCiencia/Datos-COVID19/blob/master/output/producto76/fabricante_t.csv
# ISCI Producto movilidad por comunas ->  https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto82



