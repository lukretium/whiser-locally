import subprocess
import numpy as np
import sounddevice as sd
import pyperclip
import os
import wave
import time
import argparse
from pynput import keyboard

# --- ARGUMENT PARSER ---
parser = argparse.ArgumentParser(description="M1 Whisper Dictation")
parser.add_argument("--model", type=str, default="base", 
                    choices=["base", "small", "large-v3-turbo"], 
                    help="Choose model: base, small, or large-v3-turbo")
args = parser.parse_args()

# --- CONFIG ---
MODEL_PATH = os.path.expanduser(f"~/models/ggml-{args.model}.bin")
FS = 16000 
TEMP_FILE = "/tmp/voice_prompt.wav"

# FIND THE BINARY AUTOMATICALLY
WHISPER_BIN = subprocess.run(["which", "whisper-cli"], capture_output=True, text=True).stdout.strip()

def play_sound(name="Tink"):
    os.system(f"afplay /System/Library/Sounds/{name}.aiff &")

if not WHISPER_BIN:
    print("❌ Error: Could not find 'whisper-cli'.")
    print("Please run: brew install whisper-cpp")
    exit()

print(f"🚀 Using Model: {args.model.upper()}")
print(f"🛠️  Using Binary: {WHISPER_BIN}")
print("✅ Ready! Hold Right-Ctrl to speak.")

recording = []
is_recording = False

def process_audio():
    global recording, is_recording
    is_recording = False
    if len(recording) < 15: 
        recording = []
        return
    
    start_total = time.perf_counter()
    play_sound("Pop")
    
    # 1. Save Audio
    audio_data = np.concatenate(recording, axis=0)
    with wave.open(TEMP_FILE, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(FS)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())

    try:
        # 2. Transcribe
        # GGML_METAL_PATH_RESOURCES helps the M1 use the GPU/Neural Engine
        env = os.environ.copy()
        brew_prefix = subprocess.getoutput("brew --prefix whisper-cpp")
        if brew_prefix:
            env["GGML_METAL_PATH_RESOURCES"] = f"{brew_prefix}/share/whisper-cpp"
        
        start_inference = time.perf_counter()
        
        # -l auto: Auto-detect language
        # -nt: No timestamps
        cmd = [WHISPER_BIN, "-m", MODEL_PATH, "-f", TEMP_FILE, "-l", "auto", "-nt"]
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
        
        result = proc.stdout.strip()
        end_inference = time.perf_counter()
        
        if result:
            # Get the actual text (last line of output)
            clean_text = result.split('\n')[-1].strip()
            print(f"\n✨ {clean_text}")
            pyperclip.copy(clean_text)
            os.system('osascript -e "tell application \\"System Events\\" to keystroke \\"v\\" using {command down}"')
            
            # --- DIAGNOSTICS ---
            inf_time = end_inference - start_inference
            total_time = time.perf_counter() - start_total
            print(f"⏱️  AI Inference: {inf_time:.2f}s")
            print(f"⌛ Total Process: {total_time:.2f}s")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    recording = []

def on_press(key):
    global is_recording
    if key == keyboard.Key.ctrl_r and not is_recording:
        is_recording = True
        play_sound("Tink")

def on_release(key):
    if key == keyboard.Key.ctrl_r:
        process_audio()

with sd.InputStream(samplerate=FS, channels=1, callback=lambda indata, frames, time, status: recording.append(indata.copy()) if is_recording else None):
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()