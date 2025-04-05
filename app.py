from flask import Flask, request, jsonify, render_template, send_from_directory
import openai
import tempfile
import os
import json
import SerialConnectionToArduino

app = Flask(__name__)

# ===============================
# Lecture Quiz Game Functionality
# ===============================

# Global variables for lecture quiz game
# processed_text is expected to be a JSON array string, e.g.:
# '[{"question": "What is the capital of France?", "answer": "Paris"}, ...]'
captions_text = ""
processed_text = ""
audio_transcription = ""

START_PAGE = "start.html"
MAIN_PAGE = "show.html"
END_PAGE = "win.html"

ARDUINO = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)


DEFAULT_QUESTIONS = 5

IMAGES = [
    "/images/Wordle.png",
    "/images/Wordle.png",
    "/images/Wordle.png"
]

OPTIONS = [
    "Fabio",
    "Guy A",
    "IDK"
]

# Hardcoded API key and custom base URL (per hack.funandprofit.ai)
openai.api_key = "qTPADyqTfVaamwCEIsRksDAZIhqdvvDweogu8p242iw6WZE0sk8C05jE2w3yGtIAbX88swUBsD2GHLaCdnVC14Dy2eYFluldpnK1Pvz8pyjZMXfdwPHcz6MD9HTySKSd"
openai.api_base = "https://hack.funandprofit.ai/api/providers/openai/v1"

@app.route("/api/captions", methods=["POST"])
def api_captions():
    global captions_text, processed_text
    data = request.get_json()
    if not data or "captions" not in data:
        return jsonify({"error": "No captions provided"}), 400

    captions_text = data["captions"]

    instructions = (
        "You are a gameshow host that will receive a lecture text. Your job is to read the lecture captions, understand them, "
        "and produce exactly 2 easy questions, which are gameshow friendly meaning they are very short answers and very simple, based on the lecture with clear answers. "
        "Output your result as a JSON array where each element is an object with two keys: 'question' and 'answer'. "
        "Return only the JSON, without any additional text or markdown formatting."
    )

    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": f"Lecture Captions:\n{captions_text}"}
    ]

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-3.5-turbo-16k" if needed
            messages=messages
        )
        processed_text = completion.choices[0].message.content
    except Exception as e:
        processed_text = f"Error processing captions: {e}"
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "processed_text": processed_text}), 200

@app.route("/api/transcribe", methods=["POST"])
def api_transcribe():
    global audio_transcription
    
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    
    try:
        # Save the file temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "audio_recording.mp3")
        audio_file.save(temp_path)
        
        # Open the file in binary mode and transcribe it using Whisper
        with open(temp_path, "rb") as file:
            transcription = openai.Audio.transcribe("whisper-1", file)
        
        # Clean up the temp file
        os.remove(temp_path)
        
        if isinstance(transcription, dict) and "text" in transcription:
            audio_transcription = transcription["text"]
        else:
            audio_transcription = str(transcription)
        
        return jsonify({
            "status": "success",
            "audio_transcription": audio_transcription
        }), 200
        
    except Exception as e:
        error_message = f"Transcription failed: {str(e)}"
        print(error_message)
        return jsonify({
            "error": error_message,
            "hint": "Ensure file is in proper format and contains audible speech"
        }), 500

@app.route("/api/grade", methods=["POST"])
def api_grade():
    data = request.get_json()
    if not data or "question" not in data or "expected_answer" not in data or "user_answer" not in data:
        return jsonify({"error": "Missing parameters"}), 400
    
    question = data["question"]
    expected = data["expected_answer"]
    user_answer = data["user_answer"]
    
    prompt = (
        f"Question: {question}\n"
        f"Expected Answer: {expected}\n"
        f"User Answer: {user_answer}\n\n"
        "You are grading the user's answer against the expected answer. "
        "Be lenient - they don't need to match exactly, just demonstrate understanding of the concept. "
        "Start your response with EXACTLY ONE of these keywords: 'CORRECT:' or 'INCORRECT:' "
        "followed by a brief explanation. Make sure your response starts with one of these exact keywords."
    )
    
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        grade = completion.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"grade": grade}), 200

@app.route("/api/status", methods=["GET"])
def api_status():
    return jsonify({
        "processed_text": processed_text,
        "audio_transcription": audio_transcription
    })

@app.route("/PLACEHOLDER/Prepare/", methods = ["GET"])
def start():
    return render_template(START_PAGE, options=list(zip(OPTIONS, IMAGES)), questions=DEFAULT_QUESTIONS)

@app.route("/PLACEHOLDER/Gameshow/", methods = ["POST"])
def showtime():

    questions = request.form['counter_value']
    presenter = request.form['selected_option']

    return render_template(MAIN_PAGE)

@app.route("/PLACEHOLDER/Finale/", methods = ["GET"])
def victory():
    render_template(END_PAGE)

# ===============================
# Run the Combined App
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)