import streamlit as st
import yaml
from pymongo import MongoClient
import pandas as pd
import boto3
import json
import ast
import pdfplumber
from io import BytesIO
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)



client = MongoClient(f'mongodb+srv://{config["database"]["username"]}:{config["database"]["password"]}@coral.fnddefl.mongodb.net/?retryWrites=true&w=majority')
db = client["coral"]



def get_s3():
    s3 = boto3.resource('s3', aws_access_key_id=config["s3"]["AWS_ACCESS_KEY_ID"], aws_secret_access_key=config["s3"]["AWS_SECRET_ACCESS_KEY"])  
    return s3

def get_file(s3_filename):
    s3 = get_s3()
    obj = s3.Object(config["s3"]["bucket"], s3_filename)
    file = obj.get()['Body'].read()
    with open(f"{s3_filename}.pdf", "w") as f:
        f.write(file)


def save_file(s3_filename):
    file = get_file(s3_filename)


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


# if selected:
#     s3f="partituras/7063bbfe-54bb-489f-a8b8-3a336f488fbc_Adeste_Fideles.pdf"
#     get_file(s3f)
#     st.download_button("Download",
#                         data=f"{s3f}.pdf")