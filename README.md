# Whisper Dictation Tool

Dictation tool for macOS using Whisper-CPP. Hold a configurable key, speak, and the text will be automatically transcribed and inserted.

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

Hold the trigger key, speak, release. The text will be automatically copied and pasted.

## Options

| Argument | Default | Description |
|----------|---------|-------------|
| `--model` | `base` | Whisper model: `base`, `small`, `large-v3-turbo` |
| `--key` | `ctrl_r` | Key to hold for recording (pynput key name) |

Options are **saved automatically** to `config.json` and reused on next launch. Pass an argument explicitly to override.

```bash
# Use a different model
python3 main.py --model small

# Change the trigger key (e.g. for MacBooks without right Ctrl)
python3 main.py --key ctrl_l
python3 main.py --key f13
python3 main.py --key cmd_r
```

### Finding your key name

To discover the pynput name for any key on your keyboard, run:
```bash
python3 -c "from pynput import keyboard; keyboard.Listener(on_press=lambda k: print(k)).start(); import time; time.sleep(5)"
```
Press the key within 5 seconds — its name will be printed.
