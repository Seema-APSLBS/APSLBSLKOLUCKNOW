# Install required libraries
!pip install flask flask-ngrok pyttsx3
# app.py inside Colab
from flask import Flask, render_template_string, request, jsonify
import pyttsx3

app = Flask(__name__)
engine = pyttsx3.init()

# Define multiple stories
stories = [
    {"chapter": 1, "prompt": "tree", "text": "Rabbit asks: Can you say 'tree'?"},
    {"chapter": 2, "prompt": "cat", "text": "Kitten asks: Can you say 'cat'?"},
    {"chapter": 3, "prompt": "sun", "text": "Bird asks: Can you say 'sun'?"},
    {"chapter": 4, "prompt": "ball", "text": "Dog asks: Can you say 'ball'?"}
]

current_chapter = 1

# HTML template (inline for Colab simplicity)
template = """
<!DOCTYPE html>
<html>
<head>
    <title>StoryPlay English</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        button { padding: 10px 20px; font-size: 18px; }
        .response { margin-top: 20px; font-size: 20px; color: green; white-space: pre-line; }
    </style>
</head>
<body>
    <h1>StoryPlay English</h1>
    <h2 id="storyText">{{ story['text'] }}</h2>
    <button onclick="startListening()">🎤 Speak</button>
    <div class="response" id="response"></div>

    <script>
        let recognition;
        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = "en-US";

            recognition.onresult = function(event) {
                let spoken = event.results[0][0].transcript;
                document.getElementById("response").innerText = "You said: " + spoken;

                fetch("/listen", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ spoken: spoken })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("response").innerText += "\\n" + data.response;

                    if (data.chapter) {
                        window.location.reload();
                    }
                });
            };

            recognition.onerror = function(event) {
                document.getElementById("response").innerText = "Error: " + event.error;
            };
        } else {
            alert("Speech recognition not supported in this browser.");
        }

        function startListening() {
            if (recognition) recognition.start();
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    story = stories[current_chapter - 1]
    return render_template_string(template, story=story)

@app.route("/listen", methods=["POST"])
def listen():
    global current_chapter
    spoken_text = request.json.get("spoken", "").lower()
    target = stories[current_chapter - 1]["prompt"]

    if spoken_text == target:
        engine.say(f"Great job! You said {target}!")
        engine.runAndWait()
        response = f"Great job! You said '{target}'!"
        current_chapter += 1
        if current_chapter > len(stories):
            current_chapter = len(stories)
    else:
        engine.say(f"Nice try! Let's say {target} together.")
        engine.runAndWait()
        response = f"Nice try! Let's say '{target}' together."

    return jsonify({"spoken": spoken_text, "response": response, "chapter": current_chapter})
