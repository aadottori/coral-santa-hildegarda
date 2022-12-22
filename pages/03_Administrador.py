import streamlit as st
import streamlit_authenticator as stauth
import yaml
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Bem vindo(a), *{st.session_state["name"]}*')
    st.title('Página da Administração')
