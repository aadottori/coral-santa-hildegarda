import streamlit as st


st.set_page_config(page_title='Coral Santa Hildegarda')

st.title("""Coral Santa Hildegarda""")

st.markdown("""
"Oh, Pastor das almas, e, oh, Primeira Palavra,
pela qual temos sido todos criados! \n
Consente, consente agora em livrar-nos
de nossas misérias e nossa languidez!"
""")


col1, col2 = st.columns(2)

col1.image("./midias/coral_natal.jpeg", caption="Natal, 2022")
col2.image("./midias/coral_pascoa.jpeg", caption="Páscoa, 2022")


