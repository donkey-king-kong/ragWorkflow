import singlestoredb as s2
import os
from dotenv import load_dotenv

load_dotenv()
userName = os.getenv("USERNAME")
passWord = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")

conn = s2.connect(host=host, port=port, user=userName, password=passWord, database=database)

def createTable():
    # Connect to database
    conn = s2.connect(host=host, port=port, user=userName, password=passWord, database=database)
    
    # Execution of queries
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE vectorDB (text TEXT, vector BLOB);')
    
    # Close the connection
    # conn.close()

def dropTable():
    # Connect to database
    conn = s2.connect(host=host, port=port, user=userName, password=passWord, database=database)
    
    # Execution of queries
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            cur.execute('DROP TABLE vectorDB')
    
    # Close the connection
    # conn.close()


def queryDB(query_embedding):
    # Connect to database
    conn = s2.connect(host=host, port=port, user=userName, password=passWord, database=database)
    
    # Execution of queries
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            cur.execute('SELECT text, dot_product(vector, JSON_ARRAY_PACK(%f)) as score FROM vectorDB ORDER BY score DESC LIMIT 5', (query_embedding))
            for row in cur.fetchall():
                print(row)
    
    # Close the connection
    # conn.close()

def insertDB(text, vector):
    # Connect to database
    conn = s2.connect(host=host, port=port, user=userName, password=passWord, database=database)
    text = text.replace("\n", " ")
    with conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            cur.execute('INSERT INTO vectorDB (text, vector) VALUES (%s, JSON_ARRAY_PACK(%s))', (text, vector))

    # Close the connection
    # conn.close()