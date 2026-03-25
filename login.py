import streamlit as st
from database import create_table, add_user, login_user

def login():

    create_table()

    st.title("🌱 AgroAI System")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    # -------- LOGIN --------
    with tab1:
        st.subheader("Login")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            result = login_user(username, password)

            if result:
                st.success(f"Welcome {result[0]} 👋")
                st.session_state["logged_in"] = True
            else:
                st.error("Invalid Username or Password ❌")

    # -------- SIGN UP --------
    with tab2:
        st.subheader("Create Account")

        name = st.text_input("Full Name", key="signup_name")
        new_user = st.text_input("Username", key="signup_user")
        new_pass = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Sign Up"):
            success = add_user(name, new_user, new_pass)

            if success:
                st.success("Account Created Successfully 🎉")
            else:
                st.error("Username already exists ❌")