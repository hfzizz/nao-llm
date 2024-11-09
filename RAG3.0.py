from flask import Flask, request, jsonify
import json
import ollama
import numpy as np
import os
import time
import uuid
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
app.secret_key = "123456789"

# Initialize SBERT model for embedding
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight SBERT model; can change as needed

# Define Nao's personality and conversation template
template = """
You are Nao, a friendly chatbot from Universiti Brunei Darussalam.Keep your answer in one or two sentences.
Here is the conversation history: {context}

Question: {question}

Answer:
"""

# Define the context directory to store chat history
CONTEXT_DIR = "contexts"
if not os.path.exists(CONTEXT_DIR):
    os.makedirs(CONTEXT_DIR)

last_message_time = time.time()
current_context_file = f"{CONTEXT_DIR}/{str(uuid.uuid4())}.txt"

# Load and preprocess dataset using SBERT and Ollama for embeddings (only instructions)
def load_and_preprocess_data(dataset_path, model_name='llama3.2'):
    with open(dataset_path) as f:
        data = json.load(f)

    preprocessed_data = []
    for item in data:
        instruction = item["instruction"]
        output = item["output"]
        
        # Use SBERT for embedding
        sbert_embedding = sbert_model.encode(instruction)

        # Optionally use Ollama for embedding as well
        embedding_response = ollama.embed(model=model_name, input=instruction)
        ollama_embedding = embedding_response.get('embeddings', [None])[0]

        preprocessed_data.append({
            'instruction': instruction,
            'output': output,
            'sbert_embedding': sbert_embedding,
            'ollama_embedding': ollama_embedding
        })
    return preprocessed_data

# Function to compute combined similarity
def combined_similarity(query_embedding, data_embedding, ollama_weight=0.5, sbert_weight=0.5):
    sbert_similarity = cosine_similarity([query_embedding['sbert']], [data_embedding['sbert']])[0][0]
    ollama_similarity = cosine_similarity([query_embedding['ollama']], [data_embedding['ollama']])[0][0] if data_embedding['ollama'] is not None else 0
    return ollama_weight * ollama_similarity + sbert_weight * sbert_similarity

# Embed query using both SBERT and Ollama
def embed_query(query, ollama_model_name='llama3.2'):
    sbert_query_embedding = sbert_model.encode(query)
    ollama_query_embedding = ollama.embed(model=ollama_model_name, input=query).get('embeddings', [None])[0]
    return {
        'sbert': sbert_query_embedding,
        'ollama': ollama_query_embedding
    }

# Retrieve top K documents using SBERT and Ollama integration
def retrieve_top_k(query, preprocessed_data, model_name='llama3.2', k=3):
    query_embedding = embed_query(query, ollama_model_name=model_name)
    similarities = [
        combined_similarity(query_embedding, {
            'sbert': item['sbert_embedding'],
            'ollama': item['ollama_embedding']
        }) for item in preprocessed_data
    ]
    
    top_k_indices = np.argsort(similarities)[-k:]
    top_k_documents = [preprocessed_data[i] for i in top_k_indices]

    # Optional re-ranking step
    re_ranked_documents = sorted(
        top_k_documents,
        key=lambda doc: combined_similarity(query_embedding, {
            'sbert': doc['sbert_embedding'],
            'ollama': doc['ollama_embedding']
        }),
        reverse=True
    )

    return re_ranked_documents, max(similarities)

def generate_response(query, top_k_documents, context):
    # Ensure that doc['output'] is a string (if it's a list, join the elements)
    doc_context = " ".join([
        " ".join([str(part) for part in doc['output']]) if isinstance(doc['output'], list) else str(doc['output'])
        for doc in top_k_documents[:3]
    ])
    combined_context = context + "\n" + doc_context
    prompt = template.format(context=combined_context, question=query)

    # Remove the temperature argument
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'system', 'content': 'You are Nao, a friendly chatbot from Universiti Brunei Darussalam.'},
            {'role': 'user', 'content': prompt}
        ]
    )
    return response['message']['content']



# Main Dynamic RAG function
def dynamic_rag(query, preprocessed_data, context, model_name='llama3.2', top_k=3):
    top_k_documents, max_similarity = retrieve_top_k(query, preprocessed_data, model_name=model_name, k=top_k)
    response = generate_response(query, top_k_documents, context)
    return response

# Load and save context from/to files
def load_context(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    return ""

def save_context(context, file_path):
    with open(file_path, "w") as file:
        file.write(context)

# Dynamically generate a new context file
def new_context_file():
    return f"{CONTEXT_DIR}/{str(uuid.uuid4())}.txt"

# Flask route for the chat interface
@app.route('/chat', methods=['POST'])
def chat():
    global last_message_time, current_context_file
    data = request.json
    user_input = data.get('message')

    if user_input is None:
        return jsonify({"error": "No message provided"}), 400

    # Check for inactivity of 1 minute
    if time.time() - last_message_time > 60:
        current_context_file = new_context_file()

    # Load previous context
    context = load_context(current_context_file)

    # If user ends the conversation
    if "goodbye" in user_input.lower() or user_input.lower() in ["exit", "bye", "quit"]:
        response_text = "Nao: Goodbye! Have a great day!"
        save_context(context, current_context_file)  # Save current context
        current_context_file = new_context_file()  # Start a new context
        return jsonify({"Nao": response_text})

    # Perform RAG for generating a response
    response = dynamic_rag(user_input, preprocessed_data, context, model_name='llama3.2', top_k=3)

    # Update context
    context += f"\nUser: {user_input}\nNao: {response}"
    save_context(context, current_context_file)

    # Update last message time
    last_message_time = time.time()

    return jsonify({"response": response})

if __name__ == "__main__":
    # Path to your dataset JSON
    dataset_path = r'C:\Users\User\Desktop\chatbot_test\fineTune\scripts\datasets.json'
    preprocessed_data = load_and_preprocess_data(dataset_path, model_name='llama3.2')
    
    app.run(debug=True, host='0.0.0.0')
