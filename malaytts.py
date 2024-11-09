"""
This script is used to transcribe speech to text using Malaya Speech. but the transcribe speed is too slow.
But overral, the accuracy is good.

malayvenv is the virtual environment for malaya.
"""

import malaya_speech
import ollama
import requests
import pyaudio
import wave
import os
import time
import numpy as np

# Function to play audio using PyAudio (remains unchanged)
def play_audio(file_path):
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to transcribe the recorded audio using Malaya
def transcribe_with_malaya(audio_file):
    # Load audio file
    y, sr = malaya_speech.load(audio_file)
    # Initialize the STT model
    stt = malaya_speech.stt.deep_transducer()
    # Perform greedy decoding
    transcription = stt.greedy_decoder([y])
    transcription_text = transcription[0]  # Assuming single audio input
    print(f"Transcribed Text: {transcription_text.strip()}")
    return transcription_text.strip()

# Function to record audio with a threshold
def record_audio(file_path, threshold=500, sample_rate=16000, duration=5):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
    frames = []
    print("Listening for audio above the threshold...")

    start_time = None
    silence_time = None
    max_silence_duration = 2  # Maximum allowable silence duration
    
    while True:
        data = stream.read(1024)
        audio_data = np.frombuffer(data, dtype=np.int16)
        amplitude = np.abs(audio_data).mean()  # Calculate the mean amplitude
        
        if amplitude > threshold:
            if start_time is None:
                print("Sound detected, starting recording...")
                start_time = time.time()  # Start the recording timer
            
            silence_time = None  
            frames.append(data)

            if time.time() - start_time >= duration:
                print(f"Recording stopped after {duration} seconds.")
                break
        else:
            if start_time is not None:
                frames.append(data)
                if silence_time is None:
                    silence_time = time.time()  # Start tracking silence time
            
            if silence_time is not None and time.time() - silence_time >= max_silence_duration:
                print(f"Silence detected for {max_silence_duration} seconds, stopping recording...")
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

    if frames:
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"Audio saved to {file_path}")
    else:
        print("No audio recorded.")

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


# Main function
if __name__ == "__main__":
    conversation_history = []
    system_message = {
        'role': 'system',
        'content': 'You are a helpful, polite and informative robot named Nao from the School of Digital Sciences at University Brunei Darussalam. Keep your responses concise, engaging, and appropriate for all audiences. Please keep all responses brief, ideally one or two sentences. Use conversational language. DONT use *. "Now" might be "Nao".'
    }
    conversation_history.append(system_message)

    while True:
        # Step 1: Record and transcribe speech
        audio_file_path = "recorded_audio.wav"  # Path where the recorded audio will be saved
        record_audio(audio_file_path)  # Record audio and save it to a file
        recognized_text = transcribe_with_malaya(audio_file_path)  # Transcribe using Malaya
        if recognized_text:
            conversation_history.append({'role': 'user', 'content': recognized_text})
            # Step 2: Send the conversation history to Ollama
            stream = ollama.chat(
                model='llama3.2:1b',
                messages=conversation_history,
                stream=True,
            )
            response_text = ""
            for chunk in stream:
                response_text += chunk['message']['content']
                print(chunk['message']['content'], end='', flush=True)
            # Append Ollama's response to the conversation history
            conversation_history.append({'role': 'assistant', 'content': response_text})
            # Limit the conversation history size
            if len(conversation_history) > 10:
                conversation_history = [conversation_history[0]] + conversation_history[-9:]
            # Step 3: Send the response text to the Flask server
            send_response_to_flask(response_text)
