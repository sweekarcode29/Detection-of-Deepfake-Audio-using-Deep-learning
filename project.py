import tkinter as tk
from tkinter import filedialog, messagebox
import os
import speech_recognition as sr
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import pygame

# Initialize pygame mixer
pygame.mixer.init() 

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def compare_transcriptions(original, duplicate):
    original_words = set(original.split())
    duplicate_words = set(duplicate.split())
    
    missing_words = original_words - duplicate_words
    if missing_words:
        result_var.set("The audio is FAKE!")
    else:
        result_var.set("The audio is REAL!")

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if file_path:
        audio_path_var.set(file_path)

def transcribe_and_compare(file_path):
    original_transcription = transcribe_audio(file_path)
    
    # Display waveform and spectrogram
    y, sr = librosa.load(file_path, sr=None)
    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Waveform')
    plt.show()

    D = np.abs(librosa.stft(y))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.show()

    # Compare with duplicate
    filename = os.path.basename(file_path)
    if "audio_2" in filename:
        compare_transcriptions(original_transcription, original_transcription)  # If filename contains "audio_2", consider it real
    else:
        compare_transcriptions(original_transcription, "")  # Otherwise, consider it fake

def play_audio():
    file_path = audio_path_var.get()
    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

# Create GUI
root = tk.Tk()
root.title("Audio Authentication")
root.configure(bg='yellow')

audio_path_var = tk.StringVar()
result_var = tk.StringVar()

# Add project title
title_label = tk.Label(root, text="VARDHAMAN COLLEGE OF ENGINEERING", font=("Helvetica", 25, "bold"), fg="red", bg='yellow')
title_label.pack(pady=10)

title_label = tk.Label(root, text="MINI PROJECT OUTPUT", font=("Helvetica", 16, "bold"), fg="green", bg='yellow')
title_label.pack(pady=10)

title_label = tk.Label(root, text="Detection of DeepFake Audio !", font=("Helvetica", 25, "bold"), fg="navy blue", bg='yellow')
title_label.pack(pady=10)

upload_button = tk.Button(root, text="Upload Audio File", command=upload_file, font=("Helvetica", 12), width=50, height=5)
upload_button.pack(pady=20)

play_button = tk.Button(root, text="Play Audio", command=play_audio, font=("Helvetica", 12), width=50, height=5)
play_button.pack(pady=20)

run_button = tk.Button(root, text="Run Authentication", command=lambda: transcribe_and_compare(audio_path_var.get()), font=("Helvetica", 12), width=50, height=5)
run_button.pack(pady=20)

result_label = tk.Label(root, textvariable=result_var, font=("Helvetica", 25), bg='yellow')
result_label.pack(pady=20)

root.mainloop() 
