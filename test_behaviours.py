import qi
import sys

# Replace with your NAO robot's IP and port
NAO_IP = "192.168.1.109"  # Update with your NAO's IP
NAO_PORT = 9559  # Default port for NAOqi is 9559

# Initialize qi Application properly
try:
    app = qi.Application(["MyApp", "--qi-url=tcp://" + NAO_IP + ":" + str(NAO_PORT)])
    app.start()
    session = app.session
except RuntimeError:
    print("Can't connect to Naoqi at ip \"" + NAO_IP + "\" on port " + str(NAO_PORT))
    sys.exit(1)

def trigger_nao_behavior(behavior_name):
    try:
        # Get the ALBehaviorManager service
        behavior_manager = session.service("ALBehaviorManager")
        behavior_manager.runBehavior(behavior_name)
    except Exception as e:
        print("Error occurred: {}".format(e))

def check_subscriptions():
    try:
        memory_service = session.service("ALMemory")
        
        # Get all event names
        events = memory_service.getEventList()
        print("\nEvents available:")
        for event in events:
            # Get subscribers for each event
            subs = memory_service.getSubscribers(str(event))
            if subs:  # Only print events that have subscribers
                print("Event: " + str(event))
                print("Subscribers:", subs)
                print("---")
            
    except Exception as e:
        print("Error checking subscriptions:", str(e))

if __name__ == "__main__":
    # check_subscriptions()
    behavior_name = "animations/Stand/Emotions/Negative/Sad_1"
    print("Executing") # Replace with the correct behavior name
    trigger_nao_behavior(behavior_name)
