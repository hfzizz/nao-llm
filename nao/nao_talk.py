
"""
This script is used to talk to the NAO robot using Flask.
"""

from flask import Flask, request, jsonify, send_file
from naoqi import ALProxy, ALModule, ALBroker
import qi


app = Flask(__name__)

nao_ip = "your_nao_ip" # Update with your NAO's IP
nao_port = 9559

tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)
animatedSpeech = ALProxy("ALAnimatedSpeech", nao_ip, nao_port)
motion = ALProxy("ALMotion", nao_ip, 9559)
posture = ALProxy("ALRobotPosture", nao_ip, 9559)
audio = ALProxy("ALAudioDevice", nao_ip, 9559)

# Set the volume and speed of the speech
tts.setVolume(1.5)  # Set volume between 0.0 and 1.0
tts.setParameter("speed", 100)  # Set speed (default is 100%)
tts.setLanguage("English")

# Define body language mode (full, disabled, or random)
configuration = {"bodyLanguageMode": "contextual"}

# Play audio from Flask
@app.route("/mp3", methods=['POST'])
def play_mp3():
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            print("No file part in request")
            return "No file part", 400
        
        file = request.files['file']
        if file.filename == '':
            print("No selected file")
            return "No selected file", 400

        try:
            # Save directly to NAO's home directory
            nao_path = "/home/nao/temp.wav"
            print("Saving file to: %s" % nao_path)
            file.save(nao_path)
            
            # Create the ALAudioPlayer proxy to play the audio
            playProxy = ALProxy("ALAudioPlayer", nao_ip, nao_port)
            
            # Play the saved file using post.playFile
            print("Attempting to play the saved file...")
            id_music = playProxy.post.playFile(nao_path)
            print("File played successfully with ID: %s" % str(id_music))
            
            return "File received and played successfully", 200
            
        except Exception as inner_e:
            print("Inner error: %s" % str(inner_e))
            raise inner_e
            
    except Exception as e:
        print("Error in play_mp3: %s" % str(e))
        return "An error occurred: %s" % str(e), 500

# Talk to the NAO robot
@app.route("/talk", methods=["POST"])
def talk():
    print("Received a request to talk")
    message = request.json.get("message")  # Get the message from the request
    if message:
        animatedSpeech.say(str(message), configuration)  # Use animated speech to talk
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="No message provided"), 400
    
# Run behavior
@app.route("/run_behavior", methods=['POST'])
def run_behavior():
    session = qi.Session()
    session.connect("tcp://{}:{}".format(nao_ip, nao_port))  # Using existing variables
    behavior_manager = session.service("ALBehaviorManager")

    data = request.get_json()
    behavior_name = data.get("behavior_name")

    if behavior_name:
        if behavior_manager.isBehaviorInstalled(behavior_name):
            if not behavior_manager.isBehaviorRunning(behavior_name):
                behavior_manager.runBehavior(behavior_name)
                return jsonify({"status": "success", "message": "Behavior '{}' started.".format(behavior_name)}), 200
            else:
                return jsonify({"status": "running", "message": "Behavior '{}' is already running.".format(behavior_name)}), 200
        else:
            return jsonify({"status": "error", "message": "Behavior '{}' is not installed.".format(behavior_name)}), 400
    else:
        return jsonify({"status": "error", "message": "No behavior name provided."}), 400

# Play audio from NAO's directory
@app.route('/play_audio')
def play_audio():
    try:
        # Create the ALAudioPlayer proxy to play the audio
        playProxy = ALProxy("ALAudioPlayer", nao_ip, nao_port)
        
        # Play the audio file from NAO's directory
        file_path = "/home/nao/recordings/response.mp3"
        id_music = playProxy.post.playFile(file_path)
        return 'Audio playback initiated', 200
    except Exception as e:
        return 'Error playing audio: ' + str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)  # Run the Flask server
