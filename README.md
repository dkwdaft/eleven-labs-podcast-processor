# eleven-labs-podcast-processor

An automated, modular Python pipeline designed to convert multi-part newsletter issues of ***Becoming Occupational*** into fully processed audio podcast MP3 files using the ElevenLabs API.

## 🛠 Project Overview & Architecture

This repository contains a lightweight, modular script structure designed to process text files formatted specifically for accessibility, sentence chunking, and high-quality voice synthesis.

### Modular Code Architecture

* **`config.py`**: Centralised configuration file containing API credentials, voice identification strings, file paths, and chunking threshold limits.

* **`tts_service.py`**: The core processing module that reads the target input text, formats text strings, splits content into optimal character chunks using regular expressions (`re`), sends API calls to ElevenLabs, and merges generated audio files sequentially into a single MP3 output.

* **`main.py`**: Entry point for execution. Calls the TTS processing workflow with immediate console logging.

* **`input.text`**: Source text file containing the newsletter content (formatted in lowercase, British English, and specific phonetic spellings).

## ⚙️ Technical Requirements

* **Python**: 3.9 or higher

* **Dependencies**: `elevenlabs` SDK

* **System**: Compatible with macOS, Linux, and Windows

## 📦 Installation & Setup

### 1. Clone or Download Repository

Navigate to your working directory:

```bash
git clone https://github.com/dkwdaft/eleven-labs-podcast-processor
cd eleven-labs-podcast-processor
```

### 2. Set Up a Virtual Environment

It is recommended to use an isolated Python virtual environment (`venv`):

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Install the required ElevenLabs SDK inside the active environment:

```bash
pip install elevenlabs
```

## 🔑 Credential Configuration

Open `config.py` and set your ElevenLabs API Key and desired Voice ID:

```python
# config.py

MY_API_KEY = "your_actual_elevenlabs_api_key"
MY_VOICE_ID = "your_chosen_voice_id"

INPUT_FILE = "input.text"
OUTPUT_FILE = "issue_6_podcast.mp3"
MAX_CHARS = 4500  # Character limit per chunk for API stability
```

## 🚀 Execution Workflow

1. Place your target text inside **`input.text`**.

2. Update `OUTPUT_FILE` in `config.py` to match the target issue name (e.g., `issue_6_podcast.mp3`).

3. Run the main processing script:

```bash
python main.py
```

### Script Execution Sequence (`main.py` -> `tts_service.py`):

1. **Load Text**: Reads `input.text` using UTF-8 encoding and ensures standard lowercase formatting.

2. **Chunking**: Uses regular expression boundary detection (`re.split(r'(?<=[.!?])\s+', text)`) to divide long text documents into chunks under `MAX_CHARS` (4,500 characters) without breaking mid-sentence.

3. **Synthesis**: Converts each text chunk to speech using the ElevenLabs `eleven_multilingual_v2` model and temporary audio files (`temp_part_X.mp3`).

4. **Merge & Clean**: Concatenates all temporary MP3 binary streams into a final consolidated output file and automatically cleans up temporary files.

## 📝 Text Formatting Constraints

For optimal synthesis matching the author's authentic voice, text files placed into `input.text` should follow these formatting rules:

* Completely **lowercase** text.

* **British English** spelling conventions (e.g., *favour*, *programme*, *centred*).

* Custom phonetic spellings where specified (e.g., *"marr"*).

* Clean citation markers included.

## 📄 License & Attribution

* **Author & Lived Experience Consultant**: Danny  Watson
* **vibecoded using Google Gemini

* **Publication**: *Becoming Occupational: The Lived and Learned Journey*