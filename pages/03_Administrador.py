import streamlit as st
import streamlit_authenticator as stauth
import yaml
import datetime
from pymongo import MongoClient
import json

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

# def salvar_arquivo(arquivo):
#     with open(arquivo.name, "w") as f:
#          f.write(arquivo).getbuffer()

def salvar_musica(musica):
    musicas = db.musicas
    musica_criada = musicas.insert_one(musica)
    return musica_criada.inserted_id


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Bem vindo(a), *{st.session_state["name"]}*')
    st.title('Página da Administração')

    opcoes_tipos = ["Kyriale", "Natal", "Advento"]
    nome = st.text_input("Nome")
    tipos = st.multiselect("Tipos", options=opcoes_tipos, default=None)

    musica = {
        "Nome": nome,
        "Tipos": tipos,
        "Criação": datetime.datetime.utcnow(),
        "Criador": st.session_state["username"],
    }
    
    
    musica_criada = st.button("Salvar", on_click=salvar_musica, args=(musica,))

    if musica_criada:
        st.success('Música inserida!', icon="✅")
    # arquivo = st.file_uploader(label="Upload", type=['pdf'])

    # if arquivo:
    #     r = st.button("Upload!",
    #                 type="primary",
    #                 on_click=salvar_arquivo, args=arquivo
    #                 )

