import requests
import json
import os

# Your API key from ElevenLabs
XI_API_KEY = "sk_126113009e044ecc56802e72387fe7c334a655da873e31c4"

# Your voice ID (this is the ID of the voice you've already cloned)
VOICE_ID = "MLTKhOdgXNHiATUcJQTe"

def generate_speech(text, output_filename="output.mp3", stability=1, similarity_boost=1):
    """
    Generate speech using a cloned voice on ElevenLabs.
    
    Parameters:
      - text: The text to convert to speech.
      - output_filename: File path where the generated audio will be saved.
      - stability: Controls voice stability (0-1).
      - similarity_boost: Controls how closely the output matches your voice samples (0-1).
      
    Returns:
      - True if the speech was generated successfully, False otherwise.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": XI_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }
    
    print(f"Generating speech for text: {text[:50]}...")
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        print(f"Speech generated successfully and saved as {output_filename}")
        return True
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return False

# Example usage for testing purposes
if __name__ == "__main__":
    text_to_speak = ("Hello everyone, welcome to our gameshow. "
                     "You will be going head to head against each other answering questions based on the lecture.")
    generate_speech(text_to_speak, "fabio_output_3.mp3")
