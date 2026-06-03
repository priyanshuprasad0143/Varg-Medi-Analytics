import streamlit as st
import pandas as pd
from database import cursor


def admin_panel():

    st.title("👨‍💼 Admin Panel")

    st.subheader(
        "Registered Users"
    )

    cursor.execute("""
    SELECT
        id,
        full_name,
        email,
        username
    FROM users
    """)

    users = cursor.fetchall()

    if users:

        df = pd.DataFrame(
            users,
            columns=[
                "ID",
                "Full Name",
                "Email",
                "Username"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.success(
            f"Total Users: "
            f"{len(df)}"
        )

    else:
        st.warning(
            "No users found"
        )