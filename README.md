<p align="center"> 
  <img src="pic/nao.png" alt="Nao" width="100px" height="120px">
</p>

# nao-llm
This project focuses on integrating a fine-tuned model with Retrieval-Augmented Generation (RAG) for a Large Language Model (LLM) to enable communication with the NAO Robot. The integration allows the robot to respond, interpret commands, perform actions based on emotional context, and understand Malay language.

<h1 align="center"> NAO LLM </h1>
<h3 align="center">  ZA 3201- Intelligent System Lab </h3>
<h5 align="center"> AIR-AAI Group Project - <a href="https://ubd.edu.bn/">Universiti Brunei Darussalam</a> </h5>

<!-- TABLE OF CONTENTS -->
<h2 id="table-of-contents"> :book: Table of Contents</h2>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project"> ➤ About The Project</a></li>
    <li><a href="#overview"> ➤ Overview</a></li>
    <li><a href="#project-files-description"> ➤ Project Files Description</a></li>
    <li><a href="#getting-started"> ➤ Getting Started</a></li>
    <li><a href="#contributions"> ➤ Team Contributions</a></li>
    <li><a href="#aknowlegdements"> ➤ Acknowledgement</a></li>
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
<ul><b>Goal:</b> 
  <li>To develop a communication system for the NAO Robot, enabling it to process speech, interpret emotional context, and respond in Malay. The system allows the robot to engage in meaningful interactions, perform contextual actions, and carry out commands. </li>
</ul>

<ul>
<b>Team:</b>
<li><b>Hafiz:</b> Responsible for communication with the NAO Robot, including robot API integration, speech-to-text, text-to-speech, and body control for executing actions. </li>
<li><b>Gani & Edric:</b> Focus on integrating the LLM, handling contextual understanding, and developing AI-driven conversation flows for a responsive and contextually aware experience. </li>
</ul>
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- PROJECT FILES DESCRIPTION -->
<h2 id="project-files-description"> :floppy_disk: Project Files Description</h2>

<ul>
  <li><b>nao_talk.py</b> - This script handles interaction with the NAO robot, including text-to-speech, audio player, and running behavior/action. It utilizes the NAOqi framework to manage robot operations.</li>
  <li><b>pc_sr.py</b> - This script operates independently, handling speech recognition from PC's Mic and processing the recognized text with LLM. It then sends LLM generated response to the server component.</li>
  <li><b>fineTuneilama.py</b> - This script is designed to fine-tune Ollama 3.2 by further training it on our custom dataset.</li>
  
</ul>

<h3>Some other useful files</h3>
<ul>
  <li><b>whispertts.py</b> - Same like pc_sr.py but this uses Whisper as the TTS</li>
  <li><b>malaytts.py</b> - Same like pc_sr.py but this uses malaya-speech as the TTS.</li>
  <li><b>installed_behaviours.py</b> - Get all the installed behaviours on NAO.</li>
  <li><b>test_behaviour.py</b> - Testing the installed behaviour on NAO.</li>
  <li><b>text_extractor.py</b> - For web scraping to extract data.</li>
  <li><b>command_mapping.txt</b> - Action-Command mapping.</li>
  <li><b>emotion_mapping.txt</b> - Action-Emotion mapping.</li>
</ul>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<!-- GETTING STARTED -->
<h2 id="getting-started"> :book: Getting Started</h2>

This project was originally inspired by <a href="https://github.com/fabianbosshard/nao_meets_gpt">NAO Meets GPT</a>, which provided valuable insights and ideas during development. And also <a href="https://github.com/SYSTRAN/faster-whisper">Faster Whisper</a> for a local text-to-speech (TTS) model and <a href="https://github.com/mesolitica/malaya-speech"> malaya-speech</a>  for a local malay TTS.
  
<h3>Requirements</h3>
<ul>
  <li>NAO Robot</li>
  <li>NAO Python SDK</li>
  <li>Python 3.x environment (for pc_sr.py)</li>
  <li>Python 2.7 environment (for nao_talk.py)</li>
  <li>Any Local LLM (We use Ollama)</li>
</ul>

<h3>Setup</h3>
<p>Setting up the server component :</p>
<ol>
  <li>Install the <a href="https://www.aldebaran.com/en/support/nao-6/downloads-softwares">NAO Python SDK</a>: Follow the instructions <a href="https://support.aldebaran.com/support/solutions/articles/80001017327-python-sdk-installation-guide">here</a> to install the NAO Python SDK.</li>
  <li><strong>Install Local LLM</strong>: We use <a href="https://ollama.com/download">Ollama</a> in this case we use llama3.2:1B</li>
  <li><strong>(Optional) Only if using Whisper:</strong> Install NVIDIA libraries such as cuBLAS and cuDNN. can refer <a href="https://github.com/SYSTRAN/faster-whisper">here</a></li>
  <li><strong>Python Environments and Dependencies</strong>: Detailed, step-by-step instructions for setting up these environments and installing dependencies are provided in the following sections.</a>.
    </li>
</ol>

<h3>Scraping and Fine-Tune Model</h3>
<ol>
    <li>
      <strong>Install Dependencies</strong>:To begin using Scrapy and fine-tuning your model, make sure your virtual environment is activated. Then, navigate to the requirements folder and run the following command
      <pre><code> pip install -r requirements_RAG.txt </code></pre>
    </li>
    <li>
      <strong>Scraping the Website</strong>:To start scraping run the following command
      <pre><code>scrapy crawl website_scraper -o all_text_data.json </code></pre>
    </li>
    <li>
      <strong>FineTune Ollama Model</strong>:To start finetuning the model.Navigate to the FineTune/scripts folder and run the following command
      <pre><code>python fineTunellama.py</code></pre>
    </li>
</ol>

<h3>NAO-LLM</h3>
<ol>
    <li> Setup python virtual environment for nao_talk.py</li>
      <pre><code>python -m venv venv27 </code></pre>
    <li> Activate the virtual environment </li>
      <pre><code> venv27\Scripts\activate </code></pre>
    <li> Install dependencies. Make sure you cd to requirements folder </li>
      <pre><code> pip install -r requirements_venv27.txt </code></pre>
    <li> Start the server </li>
      <pre><code>python nao_talk.py</code></pre>
</ol>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)


<!-- CONTRIBUTION -->
<h2 id="contributions">:small_orange_diamond: Team Contributions</h2>

<p><strong>Student 1 (Hafiz):</strong></p>
<ul>
  <li>Established wireless communication between PC and NAO, integrating the language model (LLM) for seamless interaction.</li>
  <li>Implemented advanced gesture and movement synchronization with spoken responses, such as waving when saying Hello!.</li>
  <li>Created a system that detects words from user input to trigger appropriate body behaviors, ensuring that the robot confirms the user’s goal before performing any movements. (e.g., "Can you salute?" to make the robot do salute action) </li>
  <li>Worked collaboratively with the team to ensure body behaviors are accurately triggered based on conversational context.</li>
  <li>Developed a text-to-speech system that enables NAO to speak in Malay.</li>
  <li>Both Malay and English support (pc_sr.py)</li>
  <li>Local English TTS (whisphertts.py).</li>
  <li>Local Malay TTS (malaytts.py).</li>
</ul>

<p><strong>Student 2 & Student 3 (Gani & Edric):</strong></p>
<ul>
  <li>Worked on enabling the LLM to maintain context-aware dialogues, ensuring consistent conversational context over multiple interactions.</li>
  <li>Gathered additional training data to enhance the system's ability to communicate about topics such as SDS, UBD, robotics, AI, and Brunei. Explored the possibility of using RAG-based systems for improved dialogue generation.</li>
  <li>Enabled extraction of action/expression-oriented words from the conversation, passing them on to Student 1 for triggering corresponding robot body behaviors.</li>
  <li>Collaborated closely as a team to ensure the system functions cohesively and delivers smooth interaction.</li>
  <li>Collected data on the Malay language to assess the potential for training the LLM to generate responses in Malay.</li>
</ul>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<!-- ACKNOWLEDGEMENTS -->
<h2 id="acknowledgement"> 📜 Acknowledgements</h2>
This project includes references to external works and resources. For a complete list of citations, please see <a href="CITATIONS.md">citations</a>


