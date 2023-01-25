"""audio_cutter.py is a little application based on moviepy lib which takes
a video file(.mp4) and returns its audio track(.mp3). Put Gorilazz video clip for easy testing."""
import moviepy.editor
from pathlib import Path

video_file = Path('gorillaz-feel-good-inc.mp4')

video = moviepy.editor.VideoFileClip(f'{video_file}')
audio = video.audio
audio.write_audiofile(f'{video_file.stem}.mp3')
