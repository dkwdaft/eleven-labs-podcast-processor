# tts_service.py
import os
import re
from elevenlabs.client import ElevenLabs

def process_and_generate_audio(file_path, api_key, voice_id, output_filename, max_chars):
    """
    Reads from input.text, formats text to lowercase, splits at sentence 
    boundaries, calls the ElevenLabs API, and merges into a single MP3.
    """
    print(f"Reading text from {file_path}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'. Make sure it is saved in the same folder.")
        return

    # Convert text to lowercase as requested
    text = raw_text.lower()

    # Initialize the ElevenLabs client
    client = ElevenLabs(api_key=api_key)

    # Automatically split text into sentences to avoid cutting off mid-sentence
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

    print(f"Text split into {len(chunks)} API request(s) automatically.")

    temp_files = []
    
    # Process each chunk sequentially through the ElevenLabs API
    for i, chunk in enumerate(chunks, 1):
        temp_filename = f"temp_part_{i}.mp3"
        print(f"Generating audio for part {i} of {len(chunks)}...")

        try:
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

        except Exception as e:
            print(f"Error generating part {i}: {e}")
            return

    # Merge all temporary audio parts into one final podcast file
    print(f"Merging all parts into {output_filename}...")
    with open(output_filename, "wb") as outfile:
        for temp_file in temp_files:
            with open(temp_file, "rb") as infile:
                outfile.write(infile.read())
            os.remove(temp_file)  # Clean up temporary part files

    print(f"Success! Your complete podcast is saved as: {output_filename}")