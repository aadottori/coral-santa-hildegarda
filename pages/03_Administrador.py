import streamlit as st
import streamlit_authenticator as stauth
import yaml
import datetime
from pymongo import MongoClient
import boto3
import time
import json
import pandas as pd
import uuid

st.set_page_config(page_title='CSH | Administrador')

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

client = MongoClient(f'mongodb+srv://{config["database"]["username"]}:{config["database"]["password"]}@coral.fnddefl.mongodb.net/?retryWrites=true&w=majority')
db = client["coral"]

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')


tags_mongo = db.tags.find({})
j = {}
for x in tags_mongo:
    j[str(x["_id"])] = x
df = pd.DataFrame.from_dict(j, orient="index")


def upload_file_to_S3(file, bucket, s3_file):
    s3 = boto3.client('s3',
                      region_name=config["s3"]["AWS_DEFAULT_REGION"],
                      aws_access_key_id=config["s3"]["AWS_ACCESS_KEY_ID"],
                      aws_secret_access_key=config["s3"]["AWS_SECRET_ACCESS_KEY"])
    
    try:
        s3.upload_fileobj(file, bucket, s3_file)
        return True
    except FileNotFoundError:
        time.sleep(9)
        st.error('File not found.')
        return False

def criar_tag(tag):
    if len(tag)>0:
        tags = db.tags
        tag_criado = tags.insert_one(tag)
        return tag_criado.inserted_id

def salvar_musica(musica):
    musicas = db.musicas
    musica_criada = musicas.insert_one(musica)
    return musica_criada.inserted_id


if st.session_state["authentication_status"]:
    st.write(f'Bem vindo(a), *{st.session_state["name"]}*')
    st.title('Página da Administração')



    opcoes_tags = list(df["tag"])
    with st.expander("Criar música"):

        nome = st.text_input("Nome")
        tags = st.multiselect("Tags", options=opcoes_tags, default=None)
        code = str(uuid.uuid4())

        uploaded_file = st.file_uploader("Selecione um arquivo")
        if uploaded_file is not None:
            if uploaded_file.type != "application/pdf":
                st.error('Só são permitidos arquivos PDF.')
            else:
                bytes_data = uploaded_file.getvalue()

        musica = {
            "name": nome,
            "tag": tags,
            "code": code,
            "creation_date": datetime.datetime.utcnow(),
            "creator": st.session_state["username"],
        }


        musica_criada = st.button("Salvar", on_click=salvar_musica, args=(musica,))
        if musica_criada:
            with st.spinner('Carregando...'):
                upload_file_to_S3(uploaded_file, f'{config["s3"]["bucket"]}', f'partituras/{code}_{nome.replace(" ", "_")}.pdf')
            st.success('Música inserida!', icon="✅")




    with st.expander("Criar tags"):
        f'Tags disponíveis: **{", ".join(list(df["tag"]))}**.'
        novo_tag = st.text_input("Nova tag")
        tag_criado = st.button("Criar", on_click=criar_tag, args=({"tag": novo_tag},))


    authenticator.logout('Sair', 'main')
