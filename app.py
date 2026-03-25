import streamlit as st
from login import login
from dashboard import dashboard

st.set_page_config(layout="wide")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    dashboard() 