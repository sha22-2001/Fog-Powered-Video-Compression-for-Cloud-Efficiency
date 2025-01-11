import os
import shutil
from pytube import YouTube
from moviepy.editor import *

def download_youtube_audio(video_url, output_path):
    try:
        # Get the YouTube video
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream and convert it to MP3
        audio_path_temp = os.path.join(output_path, "temp_audio.mp4")
        audio_path_final = os.path.join(output_path, "output_audio.mp3")
        audio_stream.download(output_path=output_path, filename="temp_audio")
        shutil.move(audio_path_temp, audio_path_final)

        print("Audio extracted successfully and saved as output_audio.mp3")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=lFKcnao-fTE"
    output_folder = os.path.dirname(os.path.abspath(__file__))
    download_youtube_audio(video_url, output_folder)
