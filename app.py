from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, session
import openai
import tempfile
import os
import json
from services.voice_read import generate_speech

app = Flask(__name__)
app.secret_key = "quiz_game_secret_key"  # Needed for session

# ===============================
# Lecture Quiz Game Functionality
# ===============================

# Global variables for lecture quiz game
# processed_text is expected to be a JSON array string, e.g.:
# '[{"question": "What is the capital of France?", "answer": "Paris"}, ...]'
captions_text = ""
processed_text = ""
audio_transcription = ""
num_questions_to_generate = 5  # Default value
presenter_name = "Default Host"  # Default value

START_PAGE = "start.html"
MAIN_PAGE = "index.html"  # Using the actual HTML filename
END_PAGE = "win.html"

DEFAULT_QUESTIONS = 5

IMAGES = [
    "images/Wordle.png",
    "images/Wordle.png",
    "images/Wordle.png"
]

OPTIONS = [
    "Fabio",
    "Guy A",
    "IDK"
]

BACKGROUND = "images/background.jpg"

# Hardcoded API key and custom base URL (per hack.funandprofit.ai)
openai.api_key = "qTPADyqTfVaamwCEIsRksDAZIhqdvvDweogu8p242iw6WZE0sk8C05jE2w3yGtIAbX88swUBsD2GHLaCdnVC14Dy2eYFluldpnK1Pvz8pyjZMXfdwPHcz6MD9HTySKSd"
openai.api_base = "https://hack.funandprofit.ai/api/providers/openai/v1"

@app.route("/api/captions", methods=["POST"])
def api_captions():
    global captions_text, processed_text, num_questions_to_generate
    data = request.get_json()
    if not data or "captions" not in data:
        return jsonify({"error": "No captions provided"}), 400

    captions_text = data["captions"]
    print(num_questions_to_generate)

    # Use the global num_questions_to_generate
    instructions = f"""
    You are a gameshow host.
    You will be given a university lecture transcript.
    Your task is to read and understand the content, then generate exactly {num_questions_to_generate} questions.

    Each question must meet the following criteria:
    1. It should be simple and based directly on the lecture.
    2. The answer should be very short (maximum 5 words).
    3. Do not use multiple choice format.
    4. Questions should feel like they belong in a lighthearted gameshow — clear, direct, and easy to answer.

    Return a JSON array of objects, each with the following fields:
    - question (string): the generated question.
    - answer (string): the correct short answer.

    Only return the raw JSON — no additional text, formatting, or explanations.
    """

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
        print(processed_text)
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

    try:
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": 
        f"""
        Compare the user_input to the expected_answer.
        Return a JSON object with the following fields:
        1. correct (boolean): true if the user_input is acceptably correct, false otherwise.
        2. feedback (string): a short natural language message to the user about their answer.

        question: {question}
        expected_answer: {expected}
        user_input: {user_answer}
        Be reasonably lenient with paraphrasing and wording differences as long as the core meaning is the same.
        """
        }])
        content = completion.choices[0].message.content
        print(content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify(content), 200

@app.route("/api/status", methods=["GET"])
def api_status():
    global presenter_name
    return jsonify({
        "processed_text": processed_text,
        "audio_transcription": audio_transcription,
        "presenter": presenter_name
    })

# Make the start page the default route
@app.route("/", methods=["GET"])
def index():
    generate_speech("Test")
    return redirect(url_for("start"))

@app.route("/WhoWantsToBeAGraduate/Prepare", methods=["GET"])
def start():
    return render_template(START_PAGE, options=list(zip(OPTIONS, IMAGES)), questions=DEFAULT_QUESTIONS, background=BACKGROUND)

@app.route("/WhoWantsToBeAGraduate/Gameshow", methods=["POST"])
def showtime():
    global num_questions_to_generate, presenter_name
    
    # Get values from the form
    num_questions_to_generate = int(request.form.get('counter_value', DEFAULT_QUESTIONS))
    presenter_name = request.form.get('selected_option', OPTIONS[0])
    
    # Store in session if needed for persistence
    session['num_questions'] = num_questions_to_generate
    session['presenter'] = presenter_name
    
    print(f"Starting game with {num_questions_to_generate} questions and presenter: {presenter_name}")
    
    # Reset processed text to ensure new questions are generated
    global processed_text
    processed_text = ""
    
    return render_template("show.html", background=BACKGROUND)

@app.route("/tts", methods=["GET"])
def tts():
    text = request.args.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Generate a unique filename using timestamp or UUID
    import uuid
    unique_id = str(uuid.uuid4())
    output_filename = f"static/tts_output_{unique_id}.mp3"
    
    success = generate_speech(text, output_filename=output_filename)
    if success:
        return jsonify({"status": "success", "filename": output_filename}), 200
    else:
        return jsonify({"error": "Text-to-speech conversion failed"}), 500
    
@app.route("/api/arduino", methods=["GET"])
def activate_arduino():
    pass

@app.route("/WhoWantsToBeAGraduate/Finale", methods=["GET"])
def victory():
    return render_template(END_PAGE)

# ===============================
# Run the Combined App
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)