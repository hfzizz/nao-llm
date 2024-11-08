<p align="center"> 
  <img src="pic/nao.png" alt="Nao" width="100px" height="120px">
</p>

# nao-llm
This project focuses on integrating a fine-tuned model with Retrieval-Augmented Generation (RAG) for a Large Language Model (LLM) to enable communication with the NAO Robot. The integration allows the robot to respond, interpret commands, perform actions based on emotional context, and understand Malay language.

<h1 align="center"> NAO LLM </h1>
<h3 align="center">  ZA 3201- Intelligent System Lab </h3>
<h5 align="center"> Group Project - <a href="https://ubd.edu.bn/">Universiti Brunie Darussalam</a> </h5>

<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents"> :book: Table of Contents</h2>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project"> ➤ About The Project</a></li>
    <li><a href="#overview"> ➤ Overview</a></li>
    <li><a href="#project-files-description"> ➤ Project Files Description</a></li>
    <li><a href="#getting-started"> ➤ Getting Started</a></li>
    <li><a href="#references"> ➤ References</a></li>
    <li><a href="#contributions"> ➤ Contributions</a></li>
  </ol>
</details>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- ABOUT THE PROJECT -->
<h2 id="about-the-project"> :pencil: About The Project</h2>
This project aims to enhance the NAO Robot's interaction capabilities by integrating a fine-tuned language model using Retrieval-Augmented Generation (RAG) for Large Language Models (LLMs). Through this integration, the robot can engage in natural conversation, execute commands, and perform context-driven actions based on emotional cues and Malay language understanding. This project merges advanced AI with robotics to push the boundaries of human-robot interaction.
<p align="justify"> 
  
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- OVERVIEW -->
<h2 id="overview"> :cloud: Overview</h2>

<p align="justify"> 
<ul>Goal: To develop a communication system for the NAO Robot, enabling it to process speech, interpret emotional context, and respond in Malay. The system allows the robot to engage in meaningful interactions, perform contextual actions, and carry out commands.
</ul>

<ul>
Team:
<li>Hafiz: Responsible for communication with the NAO Robot, including robot API integration, speech-to-text, text-to-speech, and body control for executing actions. </li>
<li>Gani & Edric: Focus on integrating the LLM, handling contextual understanding, and developing AI-driven conversation flows for a responsive and contextually aware experience. </li>
</ul>
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- PROJECT FILES DESCRIPTION -->
<h2 id="project-files-description"> :floppy_disk: Project Files Description</h2>

<ul>
  <li><b>nao_talk.py</b> - This script handles interaction with the NAO robot, including text-to-speech, audio player, and running behavior/action. It utilizes the NAOqi framework to manage robot operations.</li>
  <li><b>pc_w_malay_sr.py</b> - This script operates independently, handling speech recognition from PC's Mic and processing the recognized text with LLM. It then sends LLM generated response to the server component.</li>
</ul>

<h3>Some other usefull files</h3>
<ul>
  <li><b>Whispertts.py</b> - Same like pc_w_malay_sr.py but this uses Whisper as the TTS</li>
  <li><b>Malayatts.py</b> - Same like pc_w_malay_sr.py but this uses malaya-speech as the TTS.</li>
  <li><b>installed_behaviours.py</b> - Get all the installed behaviours on NAO.</li>
  <li><b>Testbehaviour.py</b> - Testing the installed behaviour on NAO.</li>
</ul>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<!-- GETTING STARTED -->
<h2 id="getting-started"> :book: Getting Started</h2>

This project was originally inspired by <a href="https://github.com/fabianbosshard/nao_meets_gpt">NAO Meets GPT</a>, which provided valuable insights and ideas during development. 
  
<h3>Requirements</h3>
<ul>
  <li>NAO Robot</li>
  <li>NAO Python SDK</li>
  <li>Python 3.x environment (for pc_w_malay_sr.py)</li>
  <li>Python 2.7 environment (for nao_talk.py)</li>
  <li>Any Local LLM (We use Ollama)</li>
</ul>

<h3>Setup</h3>
1. **Install the NAO Python SDK**: Follow the instructions [here](https://support.aldebaran.com/support/solutions/articles/80001017327-python-sdk-installation-guide) to install the NAO Python SDK.
2. **Python Environments**: Create two separate Python environments, one for the server component and one for the client component. The server component requires Python 2.7, while the client component requires Python 3.x. The specific Python versions and library versions used for each component are listed [here](requirements.txt).
3. **Install Dependencies**: Ensure all required Python libraries are installed in your environments.
</p>


