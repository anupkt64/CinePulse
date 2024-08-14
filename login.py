import streamlit as st
import requests
import pandas as pd
import sqlite3




# Function to add a new user to the database
def add_user(username, password, email):
    try:
        conn = sqlite3.connect('movies.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()
        st.success("Registration successful. You can now log in.")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")

# Function to validate user credentials
def validate_user(username, password):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def login(username, password):
    user = validate_user(username, password)
    if user:
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
    else:
        st.error("Invalid username or password")

def reset_password(email):
    st.success(f"Password reset instructions have been sent to {email}")

def show_login_page():
    st.title("Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    forgot_password = st.button("Forgot Password?")
    register_button = st.button("Register")
    
    if login_button:
        login(username, password)
    
    if forgot_password:
        st.session_state['show_forgot_password'] = True

    if register_button:
        st.session_state['show_registration'] = True

def show_registration_page():
    st.title("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    register_button = st.button("Register")
    back_button = st.button("Back to Login")

    if register_button:
        add_user(username, password, email)

    if back_button:
        st.session_state['show_registration'] = False

def show_forgot_password_page():
    st.title("Forgot Password")
    
    email = st.text_input("Email")
    reset_button = st.button("Reset Password")
    back_button = st.button("Back to Login")
    
    if reset_button:
        reset_password(email)
    
    if back_button:
        st.session_state['show_forgot_password'] = False