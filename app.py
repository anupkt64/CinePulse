import streamlit as st
import requests
import pandas as pd
import sqlite3
from login import show_login_page, show_forgot_password_page, show_registration_page
from search import search

def init_db():
    conn = sqlite3.connect('movies.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT,
                        email TEXT
                    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS movies (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        year TEXT,
                        genre TEXT,
                        tmdb REAL,
                        imdb_id TEXT
                    )''')
    conn.close()

def main():
    init_db()
    

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'show_forgot_password' not in st.session_state:
        st.session_state['show_forgot_password'] = False

    if 'show_registration' not in st.session_state:
        st.session_state['show_registration'] = False



    if st.session_state['show_registration']:
        show_registration_page()
    elif st.session_state['show_forgot_password']:
        show_forgot_password_page()
    elif not st.session_state['logged_in']:
        show_login_page()
    else:
        search()

if __name__ == "__main__":
    init_db()
    main()
