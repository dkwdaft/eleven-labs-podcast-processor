# tts_service.py
import os
import re
from elevenlabs.client import ElevenLabs


def process_and_generate_audio(file_path, api_key, voice_id, output_filename, max_chars):
    print("--- PIPELINE STARTED ---")
    print(f"Reading text from: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    text = raw_text.lower()
    print(f"Text loaded successfully ({len(text)} characters).")

    if not api_key or api_key == "your_elevenlabs_api_key_here":
        print("ERROR: API key is missing or not set in config.py!")
        return

    print("Connecting to ElevenLabs API...")
    client = ElevenLabs(api_key=api_key)

    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chars:
            current_chunk += (" " if current_chunk else "") + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    print(f"Text split into {len(chunks)} chunk(s). Starting audio generation...")

    temp_files = []
    for i, chunk in enumerate(chunks, 1):
        temp_filename = f"temp_part_{i}.mp3"
        print(f"Generating part {i} of {len(chunks)}...")

        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            output_format="mp3_44100_128",
            text=chunk,
            model_id="eleven_multilingual_v2"
        )

        with open(temp_filename, "wb") as f:
            for chunk_data in audio_generator:
                f.write(chunk_data)
        temp_files.append(temp_filename)

    print(f"Merging {len(temp_files)} audio segment(s) into {output_filename}...")
    with open(output_filename, "wb") as outfile:
        for temp_file in temp_files:
            with open(temp_file, "rb") as infile:
                outfile.write(infile.read())
            os.remove(temp_file)

    print(f"--- PIPELINE COMPLETE! File saved: {output_filename} ---")