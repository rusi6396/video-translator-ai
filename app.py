import streamlit as st
import moviepy.editor as mp
import whisper
from googletrans import Translator
from gtts import gTTS
import os

st.title("🎥 AI Video Translator")

uploaded_file = st.file_uploader("Video upload karein", type=["mp4"])

if uploaded_file:
    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    if st.button("Translate Karein"):
        st.info("Processing shuru ho rahi hai...")
        # Audio nikalna
        video = mp.VideoFileClip("input.mp4")
        video.audio.write_audiofile("audio.mp3")
        # Transcription
        model = whisper.load_model("base")
        result = model.transcribe("audio.mp3")
        # Translation (Hindi)
        trans = Translator()
        text_hi = trans.translate(result['text'], dest='hi').text
        # Voice banana
        tts = gTTS(text=text_hi, lang='hi')
        tts.save("hi_audio.mp3")
        # Merge
        new_audio = mp.AudioFileClip("hi_audio.mp3")
        final = video.set_audio(new_audio)
        final.write_videofile("output.mp4")
        st.success("Taiyar hai!")
        st.video("output.mp4")
