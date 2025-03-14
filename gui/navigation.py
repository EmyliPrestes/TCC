import streamlit as st
from gui.pages import show_page
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        st.sidebar.image("./assets/logo2.png", use_column_width=True)
        selected = option_menu(
            "",
            ["Sobre o Projeto",'Detecção com Câmera ao Vivo', 'Detecção de EPIs em Arquivo', 'CheckList EPI', 'Setores e Equipamentos'], 
            icons=['info-circle', 'camera', 'file-earmark', 'check2-circle', 'tools'],  
            menu_icon="folder", 
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#ac9c8f"},
                "icon": {"color": "white", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#000000"},
                "nav-link-selected": {"background-color": "#7a695d"},
            }
        )
    return selected

def render_page(selected):
    show_page(selected)
