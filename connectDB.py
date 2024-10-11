import singlestoredb as s2
import os
from dotenv import load_dotenv
import json  #  Convert vectors to JSON

load_dotenv()
userName = os.getenv("USERNAME")
passWord = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")

# Establish connection
conn = s2.connect(host=host, port=port, user=userName, password=passWord, database=database)

def createTable():
    # Create a table with vector stored as JSON
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
             # Use JSON for storing packed vectors
            cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS vectorDB (
                    text TEXT,
                    vector JSON
                );
                '''
            ) 

def dropTable():
    # Drop the table if it exists
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            cur.execute('DROP TABLE IF EXISTS vectorDB')

def queryDB(query_embedding):
    # Query the table and rank by dot product
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            # Format query_embedding correctly
            query_vector = json.dumps(query_embedding)  # Convert list to JSON
            cur.execute(
                '''
                SELECT text, dot_product(vector, JSON_ARRAY_PACK(%s)) as score
                FROM vectorDB
                ORDER BY score DESC
                LIMIT 5;
                '''
            , (query_vector,))
            
            # Fetch and print results
            for row in cur.fetchall():
                print(row)

# Takes in the text as a string and a vector as a list
def insertDB(text, vector):
    # Insert text and vector into the database
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            # Convert the vector (list) to JSON format
            vector_json = json.dumps(vector)
            cur.execute(
                '''
                INSERT INTO vectorDB (text, vector) VALUES (%s, JSON_ARRAY_PACK(%s))
                ''', (text, vector_json)
            )  # Pass JSON-packed vector

