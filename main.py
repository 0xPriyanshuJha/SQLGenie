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

def generate_sql(query, schema_info):
    prompt = f"""
    You are a Text-to-SQL assistant for the Pagila DVD rental database. 
    Given a natural language query, your task is to generate a valid SQL query that answers the question.

    PAGILA DATABASE SCHEMA:
    {schema_info}

    IMPORTANT GUIDELINES:
    1. Use only tables and columns that exist in the schema provided.
    2. Make sure to use the exact table and column names as defined in the schema.
    3. For complex queries, use appropriate JOINs based on the foreign key relationships.
    4. Be mindful of data types when comparing values.
    5. Provide only the SQL query without explanations unless the user's query is ambiguous.
    6. For ambiguous queries, ask for clarification and suggest possible interpretations.
    7. Use appropriate aggregation functions (COUNT, SUM, AVG, etc.) when needed.
    8. Limit results when appropriate (e.g., TOP 10 films by revenue).
    9. Use PostgreSQL compatible syntax.

    EXAMPLES:
    User: "Show me all actors"
    SQL: SELECT * FROM actor;

    User: "How many films are there in each category?"
    SQL: SELECT c.name AS category_name, COUNT(fc.film_id) AS film_count FROM category c JOIN film_category fc ON c.category_id = fc.category_id GROUP BY c.name ORDER BY film_count DESC;

    User: "List customers who haven't rented anything"
    SQL: SELECT c.customer_id, c.first_name, c.last_name FROM customer c LEFT JOIN rental r ON c.customer_id = r.customer_id WHERE r.rental_id IS NULL;

    USER QUERY: {query}

    Respond with only the SQL query. If the query is ambiguous or can't be answered with the given schema, explain why and suggest how to clarify.
    SQL:"""
    
    response = genai.generate_text(
        model="gemini-pro",
        prompt=prompt
    )
    
    return response.result.strip()