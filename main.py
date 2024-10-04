from document_specific_chunk import markdown_chunk_text
from createEmbeddings import getResponse
from connectDB import queryDB, insertDB, createTable, dropTable

folder_path = "resumes"
resumeChunks = markdown_chunk_text(folder_path)

# Chunking / Embedding / Storing
for filename, chunks in resumeChunks.items():
    print(f"Chunks for {filename}:")
    for i, chunk in enumerate(chunks):
        # Embedding each chunk
        vectorEmbedding = getResponse(chunk.page_content)
        # Printing the chunk number
        print(f"Chunk {i+1}: ")
        # Store each embedding into the database
        insertDB(chunk.page_content, vectorEmbedding)

# Query
# Embed the query
query = input("Enter query: ")
queryEmbedding = getResponse(query)
# Query the database
queryDB(queryEmbedding)
