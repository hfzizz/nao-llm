"""
This script is used to save the installed behaviors of the NAO robot to a text file.
"""


import qi

# Replace with your NAO robot's IP and port
NAO_IP = "your_nao_ip"  # Update with your NAO's IP
NAO_PORT = 9559  # Default port for NAOqi is 9559

def save_installed_behaviors():
    try:
        # Initialize qi framework and create a session
        session = qi.Session()
        
        # Connect to the robot
        session.connect("tcp://%s:%d" % (NAO_IP, NAO_PORT))

        # Get the ALBehaviorManager service
        behavior_manager = session.service("ALBehaviorManager")

        # List all installed behaviors
        installed_behaviors = behavior_manager.getInstalledBehaviors()
        
        # Save the behaviors to a text file
        with open("installed_behaviors.txt", "w") as file:
            file.write("Installed Behaviors:\n")
            for behavior in installed_behaviors:
                file.write("{}\n".format(behavior))  # Changed to use .format()


        print("Installed behaviors saved to installed_behaviors.txt")

    except Exception as e:
        print("Error occurred: {}".format(e))

if __name__ == "__main__":
    save_installed_behaviors()
