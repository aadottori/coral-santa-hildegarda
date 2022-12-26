import streamlit as st
import yaml
from pymongo import MongoClient
import pandas as pd
import boto3
import json
import ast
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)



client = MongoClient(f'mongodb+srv://{config["database"]["username"]}:{config["database"]["password"]}@coral.fnddefl.mongodb.net/?retryWrites=true&w=majority')
db = client["coral"]



def get_s3():
    s3 = boto3.resource('s3', aws_access_key_id=config["s3"]["AWS_ACCESS_KEY_ID"], aws_secret_access_key=config["s3"]["AWS_SECRET_ACCESS_KEY"])  
    return s3



st.set_page_config(page_title='CSH | Partituras')
st.title("""Partituras do Coral""")
st.text("Aqui encontramos todas as partituras!")


#Query no Mongo
musicas_mongo = db.musicas.find({})
j = {}
for x in musicas_mongo:
    j[str(x["_id"])] = x
df_from_j = pd.DataFrame.from_dict(j, orient="index")
df = df_from_j.copy()
df = df[["name", "tag", "code", "creation_date"]] 
# df["Download"] = st.download_button("Baixar", 


def preparar_arquivo(nome_musica):
    codigo = list(df[df["name"]==nome_musica]["code"])[0]
    s3_filename = f'partituras/{codigo}_{nome_musica.replace(" ", "_")}.pdf'
    s3 = get_s3()
    obj = s3.Object(config["s3"]["bucket"], s3_filename)
    file = obj.get()['Body'].read()
    with open(f"./{nome_musica}.pdf", "wb") as f:
        f.write(file) 


#FILTROS
st.subheader("Filtros")

selecao_titulo = st.multiselect(
    "Filtrar por título", options=df["name"].unique(), default=None
    )

df["tag"] = df["tag"].apply(lambda x: ast.literal_eval(x) if type(x)==str else x)
tags = list(set([x for y in [a for a in list(df["tag"]) for b in a] for x in y]))

selecao_tag = st.multiselect(
    "Filtrar por tag", options=tags, default=None
    )

#PARTITURAS
st.subheader("Partituras")

def make_aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=True,
        theme='streamlit', #Add theme color to the table
        enable_enterprise_modules=True,
        height=350, 
        width='100%',
        reload_data=False
    )

    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    return selected


if selecao_titulo == [] and selecao_tag == []:
    selected = make_aggrid(df)

elif selecao_titulo != [] and selecao_tag == []:
    df = df[df["name"].isin(selecao_titulo)]
    selected = make_aggrid(df)

elif selecao_titulo == [] and selecao_tag != []:
    df["Check"] = df["tag"].apply(lambda r: any(i in r for i in selecao_tag))
    df = df[df["Check"]==True]
    df = df[df.columns[0:len(df.columns)-1]]
    selected = make_aggrid(df)

else:
    df["Check"] = df["tag"].apply(lambda r: any(i in r for i in selecao_tag))
    df = df[df["Check"]==True]
    df = df[df.columns[0:len(df.columns)-1]]
    df = df[df["name"].isin(selecao_titulo)]
    selected = make_aggrid(df)




st.subheader("Download")
filtro_download = st.multiselect("Filtrar por título", options=df["name"].unique(), default=None, max_selections=1)
if filtro_download:
    nome_musica = filtro_download[0]
    preparar = st.button("Preparar", on_click = preparar_arquivo(nome_musica))

    if preparar:
        with open(f"./{nome_musica}.pdf", "rb") as f:
            download = st.download_button("Download", f, file_name=f'{nome_musica}.pdf', mime='application/pdf')