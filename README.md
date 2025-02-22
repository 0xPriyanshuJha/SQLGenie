# SQLGenie Text-to-SQL Agent for Pagila Database

This project is a Streamlit-based Text-to-SQL interface that allows users to input natural language queries and retrieve structured SQL queries for execution on a PostgreSQL database. It uses Google Gemini AI to generate SQL queries from user input.

## Features
- Converts natural language queries into SQL.
- Executes SQL queries on a PostgreSQL database.
- Displays query results in a tabular format.
- Handles schema-based query generation with guidelines to improve accuracy.

## Setup and Installation

### Prerequisites
- Python 3.8+
- PostgreSQL database with the Pagila schema
- Google Gemini API key

### Step 1: Clone the Repository
```sh
git clone https://github.com/0xPriyanshuJha/SQLGenie
cd SQLGenie
```

### Step 2: Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Step 3: Install Dependencies
```sh
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the project directory and add the following details:
```
GEMINI_API_KEY=<your_google_gemini_api_key>
DB_NAME=<your_database_name>
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_HOST=<your_database_host>
DB_PORT=<your_database_port>
```

### Step 5: Run the Application
```sh
streamlit run app.py
```

## Usage
1. Enter a natural language query in the text area (e.g., "Show the top 10 actors by number of films").
2. Click on "Generate & Run SQL".
3. The application will generate an SQL query and execute it.
4. Results will be displayed in a tabular format.

## Example Queries
- "List all customers who haven't rented anything."
- "Show the top 10 films by revenue."
- "How many films are there in each category?"

## Troubleshooting
- Ensure the PostgreSQL database is running and accessible.
- Check `.env` file for correct credentials.
- Verify that the Google Gemini API key is valid.
- If queries fail, check the schema information to ensure table and column names are correct.

## Contributions
Feel free to fork the repository and submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.

