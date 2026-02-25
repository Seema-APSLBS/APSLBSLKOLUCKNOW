from flask import Flask, render_template, request, jsonify
import pyttsx3

app = Flask(__name__)
engine = pyttsx3.init()

stories = [
    {"chapter": 1, "prompt": "tree", "text": "Rabbit asks: Can you say 'tree'?"},
    {"chapter": 2, "prompt": "cat", "text": "Kitten asks: Can you say 'cat'?"},
    {"chapter": 3, "prompt": "sun", "text": "Bird asks: Can you say 'sun'?"},
    {"chapter": 4, "prompt": "ball", "text": "Dog asks: Can you say 'ball'?"}
]

current_chapter = 1

@app.route("/")
def index():
    story = stories[current_chapter - 1]
    return render_template("index.html", story=story)

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

if __name__ == "__main__":
    app.run(debug=True)
