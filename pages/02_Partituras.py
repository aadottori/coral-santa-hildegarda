import streamlit as st
import yaml
from pymongo import MongoClient
import pandas as pd
import json
import ast
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)



client = MongoClient(f'mongodb+srv://{config["database"]["username"]}:{config["database"]["password"]}@coral.fnddefl.mongodb.net/?retryWrites=true&w=majority')
db = client["coral"]


st.set_page_config(page_title='CSH | Partituras')
st.title("""Partituras do Coral""")
st.text("Aqui encontramos todas as partituras!")


#Query no Mongo
musicas_mongo = db.musicas.find({})
j = {}
for x in musicas_mongo:
    j[str(x["_id"])] = x
df = pd.DataFrame.from_dict(j, orient="index")



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

if selecao_titulo == [] and selecao_tag == []:
    df

elif selecao_titulo != [] and selecao_tag == []:
    df[df["name"].isin(selecao_titulo)]

elif selecao_titulo == [] and selecao_tag != []:
    df["Check"] = df["tag"].apply(lambda r: any(i in r for i in selecao_tag))
    df = df[df["Check"]==True]
    df = df[df.columns[0:len(df.columns)-1]]
    df

else:
    df["Check"] = df["tag"].apply(lambda r: any(i in r for i in selecao_tag))
    df = df[df["Check"]==True]
    df = df[df.columns[0:len(df.columns)-1]]
    df = df[df["name"].isin(selecao_titulo)]
    df
