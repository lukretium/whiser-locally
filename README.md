# Whisper Dictation Tool

Dictation tool for macOS using Whisper-CPP. Hold the right Ctrl key, speak, and the text will be automatically transcribed and inserted.

## Installation

1. Install Whisper-CLI:
```bash
brew install whisper-cpp
```

2. Download base model:
```bash
mkdir -p ~/models
curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin -o ~/models/ggml-base.bin
```

3. Install Python dependencies:
```bash
uv sync
```

## Usage

```bash
python3 main.py
```

Hold the **right Ctrl key**, speak, release. The text will be automatically copied and pasted.

Other models: `python3 main.py --model small` or `--model large-v3-turbo`
