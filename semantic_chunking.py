import re
from createEmbeddings import semanticChunkingEmbeddings, getResponse
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from connectDB import queryDB, insertDB, createTable, dropTable


def chunk_text(text):
    # Split the input text into individual sentences.
    single_sentences_list = _split_sentences(text)

    # Combine adjacent sentences to form a context window around each sentence.
    combined_sentences = _combine_sentences(single_sentences_list)
    
    # Convert the combined sentences into vector representations using a neural network model.
    embeddings = convert_to_vector(combined_sentences)
    
    # Calculate the cosine distances between consecutive combined sentence embeddings to measure similarity.
    distances = _calculate_cosine_distances(embeddings)
    
    breakpoint_percentile_threshold = 50
    breakpoint_distance_threshold = np.percentile(distances, breakpoint_percentile_threshold)

    # Find all indices where the distance exceeds the calculated threshold, indicating a potential chunk breakpoint.
    indices_above_thresh = [i for i, distance in enumerate(distances) if distance > breakpoint_distance_threshold]

    # Initialize the list of chunks and a variable to track the start of the next chunk.
    chunks = []
    start_index = 0

    # Loop through the identified breakpoints and create chunks accordingly.
    for index in indices_above_thresh:
        chunk = ' '.join(single_sentences_list[start_index:index+1])
        chunks.append(chunk)
        start_index = index + 1
    
    # If there are any sentences left after the last breakpoint, add them as the final chunk.
    if start_index < len(single_sentences_list):
        chunk = ' '.join(single_sentences_list[start_index:])
        chunks.append(chunk)
    
    # Return the list of text chunks.
    return chunks

def _split_sentences(text):
    # Use regular expressions to split the text into sentences based on punctuation followed by whitespace.
    sentences = re.split(r'(?<=[.?!])\s+', text)
    return sentences

def _combine_sentences(sentences):
    # Create a buffer by combining each sentence with its previous and next sentence to provide a wider context.
    combined_sentences = []
    for i in range(len(sentences)):
        combined_sentence = sentences[i]
        if i > 0:
            combined_sentence = sentences[i-1] + ' ' + combined_sentence
        if i < len(sentences) - 1:
            combined_sentence += ' ' + sentences[i+1]
        combined_sentences.append(combined_sentence)
    return combined_sentences

def convert_to_vector(texts):
    response = semanticChunkingEmbeddings(texts)
    print(type(response))
    embeddings_list = [embedding.embedding for embedding in response.data]
    print(type(embeddings_list))
    return embeddings_list

def _calculate_cosine_distances(embeddings):
    # Calculate the cosine distance (1 - cosine similarity) between consecutive embeddings.
    distances = []
    for i in range(len(embeddings) - 1):
        similarity = cosine_similarity([embeddings[i]], [embeddings[i + 1]])[0][0]
        distance = 1 - similarity
        distances.append(distance)
    return distances

# The chunk_text and helper functions remain unchanged...

# Define the directory containing the resumes
resume_directory = 'resumes'

# Function to process all resume files in a folder
def process_resume_folder_semantic_chunking(folder_path):
    for filename in os.listdir(folder_path):
        # Only process Markdown files
        if filename.endswith('.md'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                chunks = chunk_text(text)
                print(f'Chunks for {filename}:')
                for i, chunk in enumerate(chunks):
                    print("=====================================================\n")
                    vectorEmbedding = getResponse(chunk)
                    try: 
                        print(f"Chunk {i+1}: Inserting into databse...")
                        print("=====================================================\n")
                        print(chunk)
                        insertDB(chunk, vectorEmbedding)
                    except Exception as e:
                        print(f"Error inserting into database.\nDropping table....")
                        dropTable()
                        quit()

            print(f'Finished processing {filename}\n')
