import streamlit as st
from time import sleep
from navigation import make_sidebar
import mysql.connector
import pandas as pd

import os

#-----------------------Page Config-------------------
st.set_page_config(page_title="Zein Retrieval-Augmented Generation (RAG) Gemnini✨", page_icon="GIF/icon_sm.gif")
st.subheader("Version 1.1.1")
st.image("GIF/main_gif.gif")
st.title("Zein Retrieval-Augmented Generation (RAG) Gemnini✨")
st.subheader("Powered by Langchain & Google Generative AI")

make_sidebar()
hostdb=st.secrets['DB_Host']
userdb=st.secrets['DB_User']
passworddb=st.secrets['DB_Password']
databasedb=st.secrets['DB_Database']

# Connect the password
def authenticate(username, password):
    try:
        conn = mysql.connector.connect(
            host=hostdb,
            user=userdb,
            password=passworddb,
            database=databasedb,
            port=28389
        )

        cursor = conn.cursor()
        query = "SELECT username, password FROM master_user WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        
        # Mengambil satu baris hasil
        row = cursor.fetchone()

        # Jika row tidak None, berarti username dan password cocok
        if row is not None:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return False

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

username = st.text_input("Username")
# Uppercase the username
password = st.text_input("Password", type="password")


if st.button("Log in", type="primary"):
    if authenticate(username, password):
        st.session_state.logged_in = True
        st.session_state.username = username  
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/RAG.py")
    else:
        st.error("Incorrect username or password")