import streamlit as st
import psycopg2
import google.generativeai as genai
from dotenv import load_dotenv
import os

# loading env variables
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASSWORD"), 
        host=os.getenv("DB_HOST"), 
        port=os.getenv("DB_PORT")
    )

