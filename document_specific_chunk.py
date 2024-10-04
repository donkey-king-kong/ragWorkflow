from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def markdown_chunk_text(folder_path, chunk_size=1000, chunk_overlap=50):
    resumeChunks = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            file_path = os.path.join(folder_path, filename)

            loader = UnstructuredMarkdownLoader(file_path, encoding = "utf-8")
            resume_docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                separators = ['\n##', '\n###', '\n####', '\n'],
                chunk_size = chunk_size,
                chunk_overlap = chunk_overlap
            )

            chunks = text_splitter.split_documents(resume_docs)

            resumeChunks[filename] = chunks
        
    return resumeChunks
