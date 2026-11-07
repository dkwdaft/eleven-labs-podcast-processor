# main.py
import sys
from config import MY_API_KEY, MY_VOICE_ID, INPUT_FILE, OUTPUT_FILE, MAX_CHARS
from tts_service import process_and_generate_audio

if __name__ == "__main__":
    print("Script triggered directly.", flush=True)
    process_and_generate_audio(
        file_path=INPUT_FILE,
        api_key=MY_API_KEY,
        voice_id=MY_VOICE_ID,
        output_filename=OUTPUT_FILE,
        max_chars=MAX_CHARS
    )