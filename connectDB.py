import singlestoredb as s2
import os
from dotenv import load_dotenv
import json  # Convert vectors to JSON

load_dotenv()
userName = os.getenv("USERNAME")
passWord = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")

# Create a connection function to reuse in each operation
def get_connection():
    return s2.connect(host=host, port=port, user=userName, password=passWord, database=database)

def createTable():
    # Create a new connection
    conn = get_connection()
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            # Create table
            cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS vectorDB (
                    text TEXT,
                    vector BLOB
                );
                '''
            )

def dropTable():
    # Create a new connection
    conn = get_connection()
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            cur.execute('DROP TABLE IF EXISTS vectorDB')

def queryDB(query_embedding):
    # Create a new connection
    conn = get_connection()
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            # Convert query_embedding to JSON
            query_embedding = json.dumps(query_embedding)
            cur.execute(
                '''
                SELECT text, dot_product(vector, JSON_ARRAY_PACK(%s)) as score
                FROM vectorDB
                ORDER BY score DESC
                LIMIT 5;
                ''', 
                (query_embedding)
            )
            # Fetch and print results
            for row in cur.fetchall():
                print(row[0])

def insertDB(text, vector):
    # Create a new connection
    conn = get_connection()
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            # Convert vector to JSON
            vector = json.dumps(vector)
            cur.execute(
                '''
                INSERT INTO vectorDB (text, vector) VALUES (%s, JSON_ARRAY_PACK(%s))
                ''', (text, vector)
            )