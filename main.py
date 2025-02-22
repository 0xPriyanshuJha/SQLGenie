import streamlit as st
import psycopg2
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Loading environment variables
load_dotenv()

# Configuring the Gemini AI key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def connect_db():
    """Connect to PostgreSQL"""
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"), 
            user=os.getenv("DB_USER"), 
            password=os.getenv("DB_PASSWORD"), 
            host=os.getenv("DB_HOST"), 
            port=os.getenv("DB_PORT")
        )
    except psycopg2.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

def fetch_schema():
    """Fetch database schema information dynamically"""
    conn = connect_db()
    if not conn:
        return "Error: Could not retrieve schema."
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
        """)
        schema_data = cursor.fetchall()
        conn.close()
        
        schema_info = ""
        for table, column, dtype in schema_data:
            schema_info += f"{table}.{column} ({dtype})\n"
        
        return schema_info
    except psycopg2.Error as e:
        return f"Error fetching schema: {e}"

# generating sql query prompts
def generate_sql(query, schema_info):
    """Build a prompt for the LLM to convert natural language to SQL."""
    prompt = f"""You are a Text-to-SQL assistant for the Pagila DVD rental database. 
    Given a natural language query, your task is to generate a valid SQL query that answers the question.

DATABASE SCHEMA:
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

USER QUERY: {query}

Respond with only the SQL query. If the query is ambiguous or can't be answered with the given schema, explain why and suggest how to clarify.
SQL:
"""
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "Error: No valid SQL generated."
    except Exception as e:
        return f"Error generating SQL: {e}"

# Excecuting the process
def execute_query(sql):
    """Execute SQL query on PostgreSQL"""
    conn = connect_db()
    if not conn:
        return "Database connection failed", []

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return results, column_names
    except psycopg2.Error as e:
        conn.rollback()
        return str(e), []

# UI for the application
def main():
    """Streamlit UI"""
    st.title("Text-to-SQL Agent for Pagila Database")
    user_input = st.text_area("Enter your question:")

    if st.button("Generate & Run SQL"):
        if user_input:
            schema_info = fetch_schema()
            if "Error" in schema_info:
                st.error(schema_info)
                return

            sql_query = generate_sql(user_input, schema_info)
            st.code(sql_query, language='sql')

            if sql_query.startswith("Error"):
                st.error(sql_query)
            else:
                results, columns = execute_query(sql_query)
                if columns:
                    st.dataframe(results, columns=columns)
                else:
                    st.error(f"Query Execution Error: {results}")

if __name__ == "__main__":
    main()