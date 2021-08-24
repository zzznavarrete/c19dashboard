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


producto5_csvs = get_list_csv(5)
data_list_p5 = pd.DataFrame
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




