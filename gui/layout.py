import streamlit as st

def set_custom_styles():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #ac9c8f;  /* cor de fundo do menu */
            box-shadow: 0 9px 20px rgba(0, 0, 0, 0.6)
        }
        .main {
            background-color: #c9b6a9;  /* cor de fundo da página */
        }
        </style>
        """,
        unsafe_allow_html=True
    )