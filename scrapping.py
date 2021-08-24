
# Getting github directory
API_PATH = 'https://api.github.com/repos/MinCiencia/Datos-COVID19/git/trees/master?recursive=1'

import urllib.request, json

with urllib.request.urlopen(API_PATH) as url:
    tree = json.loads(url.read().decode())


# all data from json in dict format
tree = tree['tree']

# Define functions

import pandas as pd

### Obtiene la lista de todos los CSV de un producto en particular
def get_list_csv(product_number):
  return [x['path'] for x in tree if f"output/producto{product_number}/" in x['path'] and x['path'][-3:] == "csv"]


### Obtiene la data del CSV y extrae  
def get_csv_data(raw_path):
  url_path = f"https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/{raw_path}"
  return raw_path[:-4].split("/")[2][:10] , pd.read_csv(url_path, index_col=0)



