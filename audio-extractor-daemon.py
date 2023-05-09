import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path to the folder where OBS saves the recordings
folder_path = "/path/to/folder"

# Path to the file where the list of processed files is stored
processed_files_path = "/path/to/processed_files.txt"

# Read the list of processed files from the file
if os.path.exists(processed_files_path):
    with open(processed_files_path, "r") as f:
        processed_files = [line.strip() for line in f.readlines()]
else:
    processed_files = []

# Number of seconds to wait after the last modification of the file
wait_time = 60

# Function to extract audio from a video file
def extract_audio(video_path):
    audio_path = os.path.join(folder_path, os.path.splitext(os.path.basename(video_path))[0] + ".wav")
    subprocess.run(["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", audio_path])
    return audio_path

# Class to handle file system events (e.g., file added, modified, deleted)
class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".mp4"):
            video_path = event.src_path
            # Check if the file is not being modified
            current_time = time.time()
            last_modified_time = os.path.getmtime(video_path)
            if current_time - last_modified_time < wait_time:
                return
            # Extract the audio and add the file to the list of processed files
            audio_path = extract_audio(video_path)
            processed_files.append(os.path.basename(video_path))
            with open(processed_files_path, "a") as f:
                f.write(os.path.basename(video_path) + "\n")
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".mp4"):
            video_path = event.src_path
            # Check if the file is not being modified
            current_time = time.time()
            last_modified_time = os.path.getmtime(video_path)
            if current_time - last_modified_time < wait_time:
                return
            # Extract the audio and add the file to the list of processed files
            audio_path = extract_audio(video_path)
            processed_files.append(os.path.basename(video_path))
            with open(processed_files_path, "a") as f:
                f.write(os.path.basename(video_path) + "\n")

# Create an observer and event handler, and start the observer
observer = Observer()
event_handler = FileEventHandler()
observer.schedule(event_handler, folder_path, recursive=False)
observer.start()

# Loop indefinitely
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()