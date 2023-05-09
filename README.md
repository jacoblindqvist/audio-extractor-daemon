# Audio Extractor

This is a simple Python script that monitors a folder for newly added or modified `.mp4` video files, extracts the audio from them using FFmpeg, and saves the audio files as `.wav` files. 

## Dependencies

This script depends on the following Python libraries:

- `watchdog`
- `subprocess`

It also requires FFmpeg to be installed on your system.

## Usage

1. Install the dependencies using `pip install -r requirements.txt`
2. Set the `folder_path` variable in the script to the folder where OBS saves your recordings.
3. Set the `processed_files_path` variable to the path of a file where the list of processed files will be stored.
4. Run the script using `python audio_extractor.py`

The script will start monitoring the folder for new or modified `.mp4` files. When a new file is added or an existing file is modified, the script will wait for a certain period of time (60 seconds by default) to make sure the file is not being modified, and then extract the audio from it using FFmpeg. The audio file will be saved in the same folder as the original video file, with the same name but with the `.wav` extension.

The list of processed files will be stored in the file specified by `processed_files_path`. The script will read this file at startup and skip any files that have already been processed.

To stop the script, press `Ctrl+C`. The script will stop monitoring the folder and exit.

## License

This code is released under the MIT License. See the `LICENSE` file for more information.