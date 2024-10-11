import re
from createEmbeddings import getResponse
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
    response = getResponse(texts)
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

# Main Section
text = """# Akash Savanur

+65 81732147 | akash013@e.ntu.edu.sg | linkedin.com/in/akash-savanur |

## Education

### Nanyang Technological University, Singapore

* Bachelor of Engineering in Computer Science, Second Major in Business

**CGPA: 4.84/5.00**

Aug 2023 - July 2027

### Relevant Coursework

* Data Structures and Algorithms, Data Science and Artificial Intelligence, Digital Logic, Financial Management

## Experience

### Full Stack Development Intern

**Doozie Soft**

June 2024 - July 2024

Bangalore, India

* Engineered a full-fledged temple management website using the PERN stack (PostgreSQL, Express, React, Node.js).
* Designed and deployed 15+ microservices, reducing API response times by 40%, and handled over 2000 user registrations and 500+ payments through Razorpay with a 98% success rate.
* Integrated WhatsApp APIs for OTP generation and notifications, enhancing user authentication and engagement, along with automated audit logs and receipt generation for secure transactions.
* Managed the deployment process on AWS services, ensuring high scalability and reliability of the application, and maintained robust version control using GitHub.
* Registered over 2000 users within the beta phase, facilitated by efficient event booking and donation management features, contributing to high user satisfaction and engagement.

### Phishing Email Detection using Machine Learning

**Nanyang Technological University**

Apr 2024 - May 2024

Singapore

* Designed a Machine Learning solution to accurately classify and detect phishing emails, providing practical insights to prevent individuals from falling victim to phishing attacks in real-world scenarios.
* Utilized Logistic Regression, Random Forest, GRU Neural Network and SVM machine learning models.
* Best-performing model had an F1-score of 0.97.
* The findings of this project have practical implications in real-world scenarios, where individuals can use the developed model to identify and avoid phishing emails, thereby reducing the risk of falling victim to cyber attacks.

### Software Engineering Intern

**Excelsoft Technologies Pvt Ltd**

Apr 2022 - May 2022

Mysore, India

* Collaborated with a team of 5 developers to design and implement an employee attendance system; collaborated with system engineers, testing and QA for final delivery.
* Designed a facial recognition system using PyTorch and utilised the Django framework for implementation.
* Utilized four Machine Learning models and frameworks; Implemented convolutional neural networks and deep learning algorithms to optimise the model.

### Project Leader

**New York Academy of Sciences (NYAS)**

Nov 2021 - Jan 2022

* Led a team of 4 in the NYAS Telemedicine challenge; designed a mobile application aimed at tackling problems related to telemedicine diagnosis; enhanced data analytics competencies.

## Technical Skills

**Languages:** Java, Python, C/C++, SQL (Postgres), JavaScript, HTML/CSS, R

**Frameworks:** React, Node.js, Django, Redux, Express, Material-UI, MongoDB

**Developer Tools:** Git, Google Cloud Platform, VS Code, Visual Studio, PyCharm

**Libraries:** pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, PyTorch, Flask

## Business/Finance Skills

* NPV, IRR, MIRR, WACC, Equity markets, Bond markets, Portfolio analysis, Corporate Finance, Investments, Marketing"""
chunks = chunk_text(text)


for i, chunk in enumerate(chunks):
    print(f'chunk{i+1}')
    print(chunk)
    print()