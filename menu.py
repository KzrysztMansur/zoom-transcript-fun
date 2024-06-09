import streamlit as st


def authorized_menu():
    st.sidebar.page_link("start.py", label="Sobre nosotros")
    st.sidebar.page_link("pages/file.py", label="Archivos")
    st.sidebar.page_link("pages/zoom.py", label="Zoom")
