from faster_whisper import WhisperModel
import ollama
import requests
import pyaudio
import wave
import os
import time
import numpy as np
 
# Initialize the Whisper model
model_size = "medium.en"
whisper_model = WhisperModel(model_size, device="cuda", compute_type="float16")  # You can choose different sizes: tiny, base, small, medium, large
 
# Function to play audio using PyAudio
def play_audio(file_path):
    # Open the audio file
    wf = wave.open(file_path, 'rb')
    # Create a PyAudio Instance
    p = pyaudio.PyAudio()
    # Open a stream to play audio
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    # Read and play audio data
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    # Stop and close the stream and PyAudio instance
    stream.stop_stream()
    stream.close()
    p.terminate()
                    
# Model and device setup
#device = 'cuda' if torch.cuda is available() else 'cpu'
#output_dir = 'outputs'
#os.makedirs(output_dir, exist_ok=True)

 
# Function to transcribe the recorded audio using faster-whisper
def transcribe_with_whisper(audio_file):
    segments, info = whisper_model.transcribe(audio_file, beam_size=5)
    transcription = ""
    for segments in segments:
        transcription += segments.text + " "

    # Print transcription to the terminal
    print(f"Transcribed Text: {transcription.strip()}")
    print("")
    return transcription.strip()

def record_audio(file_path, threshold=500, sample_rate=16000, duration=5):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
    frames = []
    print("")
    print("Listening for audio above the threshold...")

    start_time = None  # To track when the actual recording starts
    silence_time = None  # To track when silence begins
    max_silence_duration = 2  # Maximum allowable silence duration
    
    while True:
        data = stream.read(1024)
        # Convert the byte data to a numpy array to analyze its amplitude
        audio_data = np.frombuffer(data, dtype=np.int16)
        amplitude = np.abs(audio_data).mean()  # Calculate the mean amplitude
        
        if amplitude > threshold:
            if start_time is None:
                print("Sound detected, starting recording...")
                start_time = time.time()  # Start the recording timer
            
            # Reset silence tracking when sound is detected
            silence_time = None  
            frames.append(data)

            # Stop recording after the specified duration
            if time.time() - start_time >= duration:
                print(f"Recording stopped after {duration} seconds.")
                break
        else:
            if start_time is not None:
                frames.append(data)  # Continue appending frames even during brief silence
                
                if silence_time is None:
                    silence_time = time.time()  # Start tracking silence time
            
            # Stop recording if amplitude is below threshold for more than 2 seconds
            if silence_time is not None and time.time() - silence_time >= max_silence_duration:
                print(f"Silence detected for {max_silence_duration} seconds, stopping recording...")
                break

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a .wav file if recording occurred
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
 
if __name__ == "__main__":
    conversation_history = []
    system_message = {
        'role': 'system',
        'content': 'You are a helpful, polite and informative robot named Nao from the School of Digital Sciences at University Brunei Darussalam. Keep your responses consice, engaging, and appropriate for all audiences. Please keep all responses brief, ideally one or two sentences. Use conversional language. DONT use *. "Now" might be "Nao" '
    }

    #initial_response = "Hello I'm Nao! a robot from the School of Digital Sciences."
    conversation_history.append(system_message)

    # Add an initial message from the assistant (NAO)
    #initial_response = "Hello, I'm Nao from the School of Digital Sciences at UBD. How can I assist you today?"
    #conversation_history.append({'role': 'assistant', 'content': initial_response})
    #print(initial_response)  # Print the initial response to simulate the introduction
    #send_response_to_flask(initial_response)

    while True:
        # Step 1: Record and transcribe speech
        audio_file_path = "recorded_audio.wav"  # Path where the recorded audio will be saved
        record_audio(audio_file_path)  # Record audio and save it to a file
        recognized_text = transcribe_with_whisper(audio_file_path)  # Transcribe the recorded audio using Whisper'
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

 