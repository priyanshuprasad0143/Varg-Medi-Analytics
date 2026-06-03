import streamlit as st
from database import (
    create_users_table,
    register_user,
    login_user
)


def auth_screen():
    create_users_table()

    st.title("🔐 Login / Signup")

    menu = [
        "Login",
        "Signup"
    ]

    choice = st.sidebar.selectbox(
        "Select Option",
        menu
    )

    # -----------------------
    # LOGIN
    # -----------------------
    if choice == "Login":

        st.subheader(
            "Login to Account"
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(
                username,
                password
            )

            if user:
                st.session_state[
                    "logged_in"
                ] = True

                st.session_state[
                    "username"
                ] = username

                st.success(
                    "Login Successful ✅"
                )

                st.rerun()

            else:
                st.error(
                    "Invalid username "
                    "or password"
                )

    # -----------------------
    # SIGNUP
    # -----------------------
    elif choice == "Signup":

        st.subheader(
            "Create New Account"
        )

        full_name = st.text_input(
            "Full Name"
        )

        email = st.text_input(
            "Email"
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Create Account"
        ):

            success = register_user(
                full_name,
                email,
                username,
                password
            )

            if success:
                st.success(
                    "Account Created "
                    "Successfully ✅"
                )

            else:
                st.error(
                    "Username or "
                    "Email already exists"
                )