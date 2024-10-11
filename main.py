from document_specific_chunk import markdown_chunk_text
from createEmbeddings import getResponse

folder_path = "resumes"
resumeChunks = markdown_chunk_text(folder_path)

for filename, chunks in resumeChunks.items():
    print(f"Chunks for {filename}:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}")
        print(getResponse(chunk.page_content))
        print()
