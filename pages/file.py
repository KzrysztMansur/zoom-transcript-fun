import streamlit as st
from menu import authorized_menu

authorized_menu()

st.title("Bienvenido al área de archivos")
st.subheader("Aquí podrás subir tus videos o audios para obtener tus anotaciones")

st.file_uploader("file_uploader", type=[".wav", ".mp4"])
st.button("Obtener anotaciones")
