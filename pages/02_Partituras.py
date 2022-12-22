import streamlit as st
import yaml
from pymongo import MongoClient
import pandas as pd

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)



client = MongoClient("mongodb+srv://coral:Vq6Xv9Y6X8CtxEP2@coral.fnddefl.mongodb.net/?retryWrites=true&w=majority")
db = client["coral"]


st.set_page_config(page_title='CSH | Partituras')
st.title("""Partituras do Coral""")

st.text("Aqui encontramos todas as partituras!")

musicas = db.musicas.find({})
# accounts = list(df.account_name.unique())
st.subheader("Filtros")


# selecao_titulo = st.multiselect(
#     "Filtrar por título", options=musicas[0].keys(), default=None
#     )

# tipos = list(set([a for b in [musicas[0][x]["Tipo"] for x in musicas[0]] for a in b]))
# selecao_tipo = st.multiselect(
#     "Filtrar por tipo", options=tipos, default=None
#     )

# st.subheader("Partituras")

# if selecao_titulo == [] and selecao_tipo == []:
#     musicas
# elif selecao_titulo != [] and selecao_tipo == []:
#     musicas_filtradas_por_nome = {}
#     for x in musicas[0]:
#         if x in selecao_titulo:
#             musicas_filtradas_por_nome[x] = musicas[0][x]
#     [musicas_filtradas_por_nome]

# elif selecao_titulo == [] and selecao_tipo != []:
#     musicas_filtradas_por_tipo = {}
#     for x in musicas[0]:
#         tipos_musica = musicas[0][x]["Tipo"]
#         if any(tipo in tipos_musica for tipo in selecao_tipo):
#             musicas_filtradas_por_tipo[x] = musicas[0][x]
#     [musicas_filtradas_por_tipo]

# else:
#     musicas_filtradas_por_nome = {}
#     for x in musicas[0]:
#         if x in selecao_titulo:
#             musicas_filtradas_por_nome[x] = musicas[0][x]
#     musicas_filtradas_por_nome = [musicas_filtradas_por_nome]
    
#     musicas_filtradas_por_nome_e_tipo = {}
#     for x in musicas_filtradas_por_nome[0]:
#         tipos_musica = musicas_filtradas_por_nome[0][x]["Tipo"]
#         if any(tipo in tipos_musica for tipo in selecao_tipo):
#             musicas_filtradas_por_nome_e_tipo[x] = musicas_filtradas_por_nome[0][x]
#     [musicas_filtradas_por_nome_e_tipo]


j = {}
for x in musicas:
    j[str(x["_id"])] = x

colunas_desejadas = ["Nome", "Tipos", "Criação"]
df = pd.DataFrame.from_dict(j, orient="index", columns=colunas_desejadas)
df
