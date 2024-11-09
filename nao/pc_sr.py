"""
Using Speech Recognition to transcribe speech to text 
and able to respond to both English and Malay.

(only SR works with Malay and English, and Whisper only works with English)

venv3 is the virtual environment for this script.
"""

import speech_recognition as sr
from gtts import gTTS
import os
import ollama
from pydub import AudioSegment
from pydub.playback import play
import requests
import paramiko
import threading
from transformers import pipeline
import time

# Update with your NAO's IP, username, and password
your_nao_ip = "your_nao_ip"
your_nao_username = "your_nao_username"
your_nao_password = "your_nao_password"

# Emotion model
emotion_model = pipeline("text-classification", model="michellejieli/emotion_text_classifier")

# Function to record audio
def record_audio():
    recognizer = sr.Recognizer()
    
    english_markers = {
    'hello', 'hi', 'hey', 'how', 'are', 'you', 'what', 'when', 'where', 'why', 'who', 
    'the', 'is', 'am', 'are', 'this', 'that', 'it', 'we', 'they', 'do', 'does', 'did', 
    'can', 'could', 'would', 'will', 'shall', 'should', 'your', 'my', 'mine', 'their', 
    'our', 'and', 'or', 'with', 'for', 'about', 'from', 'at', 'of', 'in', 'on', 'up', 
    'down', 'yes', 'no', 'please', 'thank', 'thanks', 'okay', 'really', 'know', 'think', 
    'believe', 'understand', 'like', 'want', 'need', 'good', 'bad', 'happy', 'sad', 
    'love', 'hate'
    }

    malay_markers = {
    'apa', 'bila', 'siapa', 'mengapa', 'bagaimana', 'saya', 'awak', 'anda', 'dia', 
    'mereka', 'ini', 'itu', 'dan', 'atau', 'dengan', 'kerana', 'sebab', 'jika', 'kalau', 
    'tak', 'tidak', 'boleh', 'hendak', 'mahu', 'suka', 'cinta', 'baik', 'buruk', 
    'gembira', 'sedih', 'betul', 'salah', 'tahu', 'faham', 'kenal', 'ingat', 'percaya', 
    'kami', 'kita', 'korang', 'kami', 'punya', 'jangan', 'kenapa', 'macam', 'sudah', 
    'belum', 'nanti', 'lah', 'kah', 'lah', 'ke', 'ya', 'tidak'
    }

    
    with sr.Microphone() as source:
        print("Please speak something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            try:
                malay_text = recognizer.recognize_google(audio, language='ms')
            except:
                malay_text = None

            try:
                english_text = recognizer.recognize_google(audio, language='en-US')
            except:
                english_text = None

            # If we got both translations, use word markers to help determine language
            if malay_text and english_text:
                english_count = sum(1 for word in english_text.lower().split() if word in english_markers)
                malay_count = sum(1 for word in malay_text.lower().split() if word in malay_markers)
                
                # If we found marker words, use them to determine language
                if english_count > 0 or malay_count > 0:
                    return {'text': english_text, 'is_malay': False} if english_count >= malay_count else {'text': malay_text, 'is_malay': True}
                
                # Fallback to word count if no markers found
                malay_words = len(malay_text.split())
                english_words = len(english_text.split())
                return {'text': english_text, 'is_malay': False} if english_words > malay_words else {'text': malay_text, 'is_malay': True}
            
            # If only one language was recognized, use that
            elif malay_text:
                return {'text': malay_text, 'is_malay': True}
            elif english_text:
                return {'text': english_text, 'is_malay': False}
            else:
                raise sr.UnknownValueError()
            
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# Function to save response text as mp3 file
def save_mp3(response_text):
    tts = gTTS(text=response_text, lang='ms')  # Use 'ms' for Malay
    tts.save("response.mp3")  # Save the audio file

# Function to play response text as mp3 file for testing purpose
def respond_with_gtts(response_text):
    # Convert the response text to speech
    tts = gTTS(text=response_text, lang='ms')  # Use 'ms' for Malay
    tts.save("response.mp3")  # Save the audio file

    # Check if the file was created
    if os.path.exists("response.mp3"):
        # print("MP3 file created successfully.")
        # Load and play the audio file
        audio = AudioSegment.from_mp3("response.mp3")
        play(audio)  # Play the audio file
        os.remove("response.mp3")  # Remove the audio file after playing
    else:
        print("Error: response.mp3 was not created.")

# Function to send response text to the Flask server
def send_response_to_flask(response_text):
    try:
        url = 'http://localhost:5004/talk'  # Replace with your Flask server's URL
        payload = {"message": response_text}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Response sent to Flask server successfully.")
        else:
            print(f"Failed to send response to Flask server: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while sending response to Flask server: {e}")

# Load behavior mapping from the text file
def load_behavior_mapping(file_path):
    behavior_mapping = {}
    with open(file_path, 'r') as file:
        for line in file:
            behavior, keywords = line.strip().split(':')
            behavior_mapping[behavior] = keywords.split(',')
    return behavior_mapping

# Load behavior mapping from the text file
behavior_mapping = load_behavior_mapping("command_mapping.txt")
emotion_mapping = load_behavior_mapping("emotion_mapping.txt")

# Function to find the behavior to run based on the transcribed text
def find_behavior(text):
    for behavior, keywords in behavior_mapping.items():
        if any(keyword in text.lower() for keyword in keywords):
            return behavior
    return None

# Function to find the behavior to run based on the emotion word
def find_emotion_action(emotion_word):
    # Load emotion mappings from file
    with open('emotion_mapping.txt', 'r') as f:
        emotion_mappings = dict(line.strip().split(': ') for line in f if line.strip())
    
    # Reverse the mapping since we want to look up by emotion name
    reversed_mappings = {v: k for k, v in emotion_mappings.items()}
    
    # Look up the animation path for the given emotion word
    return reversed_mappings.get(emotion_word.lower())

# Function to upload file to NAO    
def upload_file_to_nao(local_file_path, nao_ip, nao_port, nao_username, nao_password):
    # Connect to the NAO robot
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(nao_ip, port=nao_port, username=nao_username, password=nao_password)

    # Use SCP to upload the file
    sftp = ssh.open_sftp()
    remote_file_path = '/home/nao/recordings/' + local_file_path.split('/')[-1]
    sftp.put(local_file_path, remote_file_path)
    sftp.close()
    ssh.close()

    print(f"File uploaded to {remote_file_path}")

# Function to send a request to the Flask server to run a behavior
def run_behavior(behavior_name):
    try:
        url = 'http://localhost:5004/run_behavior'  # Your Flask server URL and endpoint
        payload = {"behavior_name": behavior_name}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Behavior '{behavior_name}' triggered successfully on NAO.")
        else:
            print(f"Failed to trigger behavior on NAO: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while triggering behavior on NAO: {e}")

# Function to clean text
def clean_text(text):
    # Remove specific markers or headers
    text = text.replace("<|start_header_id|>", "").replace("<|end_header_id|>", "")
    return text.strip()

# Function to execute actions in parallel
def execute_actions(response_text, behavior_name):
    # Create two threads for parallel execution
    response_thread = threading.Thread(target=send_response_to_flask, args=(response_text,))
    behavior_thread = threading.Thread(target=run_behavior, args=(behavior_name,))
    
    # Start both threads
    response_thread.start()
    behavior_thread.start()
    
    # Wait for both threads to complete
    response_thread.join()
    behavior_thread.join()

# Function to play audio on NAO
def play_audio_on_nao():
    try:
        # Send request to Flask endpoint to play audio
        response = requests.get('http://localhost:5004/play_audio')
        if response.status_code == 200:
            print("Audio playback request sent successfully")
        else:
            print(f"Failed to send playback request: {response.status_code}")
    except Exception as e:
        print(f"Error sending playback request: {e}")

# Main function
if __name__ == "__main__":
    conversation_history = []
    system_message = {
        'role': 'system',
        'content': 'You are Nao, a helpful and emotional robot from the School of Digital Sciences at University Brunei Darussalam. Keep responses to 1-2 sentences. IMPORTANT: If the user message is in English, you MUST respond in English. If the user message is in Malay, you MUST respond in Malay.'
    }
    conversation_history.append(system_message)

    # Define greeting words
    greeting_words = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']

    while True:
        result = record_audio()
        if result:
            recognized_text = result['text']
            print("Transcribed text: ", recognized_text)
            is_malay = result['is_malay']
            print("Is Malay: ", is_malay)

            # Add language indicator to the user message
            language_prefix = "[MALAY]" if is_malay else "[ENGLISH]"
            conversation_history.append({
                'role': 'user', 
                'content': recognized_text  # Remove the language prefix
            })

            if is_malay: #malay
                
                stream = ollama.chat(
                    model='llama3.2:1b',
                    messages=conversation_history,
                    stream=True,
                )
                response_text = ""
                for chunk in stream:
                    response_text += chunk['message']['content']
                    print(chunk['message']['content'], end='', flush=True)

                cleaned_response_text = clean_text(response_text)

                emotion_response = emotion_model(cleaned_response_text)[0]
                emotion_label_malay = emotion_response['label']
                print("Malay emotion label: ", emotion_label_malay)

                # Append Ollama's response to the conversation history
                conversation_history.append({'role': 'assistant', 'content': cleaned_response_text})
                # For Malay text, use TTS + upload + play approach
                save_mp3(cleaned_response_text)
                upload_file_to_nao('response.mp3', your_nao_ip, 22, your_nao_username, your_nao_password)
                play_audio_on_nao()
            
            else: #english     
                if recognized_text:
                    # Check for behavior in the transcribed text
                    behavior_to_run = find_behavior(recognized_text)
                
                    if behavior_to_run:
                        # Ask for confirmation
                        confirmation_message = f"Should I do that now?"
                        print(confirmation_message)
                        send_response_to_flask(confirmation_message)
                    
                        # Record and transcribe confirmation response
                        result = record_audio()
                        recognized_text = result['text']
                        confirmation_text = recognized_text
                    
                        # Add confirmation interaction to conversation history
                        conversation_history.append({'role': 'assistant', 'content': confirmation_message})

                        # Check if confirmation is positive
                        if any(word in confirmation_text.lower() for word in ['yes', 'yeah', 'sure', 'okay', 'please']):
                            run_behavior(behavior_to_run)
                            # Add behavior execution to conversation history
                            conversation_history.append({
                                'role': 'assistant', 
                                'content': f"I am executing the {behavior_to_run.replace('_', ' ')} behavior."
                            })

                        

                    stream = ollama.chat(
                        model='llama3.2:1b',
                        messages=conversation_history,
                        stream=True,
                    )
                    response_text = ""
                    for chunk in stream:
                        response_text += chunk['message']['content']
                        print(chunk['message']['content'], end='', flush=True)

                    cleaned_response_text = clean_text(response_text)
                    emotion_response = emotion_model(cleaned_response_text)[0]
                    emotion_label = emotion_response['label']
                    print("English emotion label: ", emotion_label)

                   
                    emotion_action = find_emotion_action(emotion_label)
                    print("English emotion action: ", emotion_action)

                    # Append Ollama's response to the conversation history
                    conversation_history.append({'role': 'assistant', 'content': response_text})
                    
                    if any(word.lower() in recognized_text.lower() for word in greeting_words):
                        print(cleaned_response_text)
                        execute_actions(cleaned_response_text, "dialog_hello/bhr_wave")
                    else:
                        # send_response_to_flask(cleaned_response_text)
                        execute_actions(cleaned_response_text, emotion_action)

                    # Limit the conversation history size
                    if len(conversation_history) > 10:
                        conversation_history = [conversation_history[0]] + conversation_history[-9:]

