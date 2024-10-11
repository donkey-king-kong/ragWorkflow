from document_specific_chunk import markdown_chunk_text
from createEmbeddings import getResponse
from connectDB import queryDB, insertDB, createTable, dropTable
from semantic_chunking import process_resume_folder_semantic_chunking

folder_path = "resumes"
# documentSpecificChunk = markdown_chunk_text(folder_path)
# semanticChunking = 

def choose_chunking_method(folder_path):
    print("Choose a chunking method:")
    print("1. Semantic Chunking")
    print("2. Document based Chunking")
    choice = input("Enter 1 or 2: ")
    if choice == '1':
        return process_resume_folder_semantic_chunking(folder_path)
    elif choice == '2':
        documentSpecificChunk = markdown_chunk_text(folder_path)
        return document_based_chunking(documentSpecificChunk)
    else:
        print("Invalid choice. Defaulting to Semantic Chunking.")
        return process_resume_folder_semantic_chunking

# Chunking / Embedding / Storing
def document_based_chunking(documentSpecificChunk):
    for filename, chunks in documentSpecificChunk.items():
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

createTable()

choose_chunking_method(folder_path)

# Query
# Embed the query
query = input("Enter query: ")
queryEmbedding = getResponse(query)
# Query the database
queryDB(queryEmbedding)
# Drop table before quitting
dropTable()
