from document_specific_chunk import markdown_chunk_text
from createEmbeddings import getResponse
from connectDB import queryDB, insertDB, createTable, dropTable

folder_path = "resumes"
resumeChunks = markdown_chunk_text(folder_path)

createTable()

# Chunking / Embedding / Storing
for filename, chunks in resumeChunks.items():
    print(f"Chunks for {filename}:")
    for i, chunk in enumerate(chunks):
        # Embedding each chunk
        print(chunk.page_content)
        print("=====================================================\n")
        vectorEmbedding = getResponse(chunk.page_content)
        # Store each embedding into the database
        try: 
            print(f"Chunk {i+1}: Inserting into databse...")
            insertDB(chunk.page_content, vectorEmbedding)
        except Exception as e:
            print(f"Error inserting into database.\nDropping table....")
            dropTable()
            quit()

# Query
# Embed the query
query = input("Enter query: ")
queryEmbedding = getResponse(query)
# Query the database
queryDB(queryEmbedding)
# Drop table before quitting
dropTable()
