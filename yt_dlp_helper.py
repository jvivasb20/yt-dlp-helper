# yt-dlp helper v1.0.0
# yt-dlp version: 2023.03.04
# Python version: 3.10.9 (tags/v3.10.9:1dd9be6, Dec  6 2022, 20:01:21) [MSC v.1934 64 bit (AMD64)]

import configparser
import os
import subprocess
import sys
import winreg

import yt_dlp

CONFIG_FILE = 'config.ini'
CONFIG_DB = 'root'


def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


def set_config(ffmpeg_location, ffprobe_location):
    config = get_config()
    config.set(CONFIG_DB, 'ffmpeg_location', ffmpeg_location)
    config.set(CONFIG_DB, 'ffprobe_location', ffprobe_location)
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)


def get_locations():
    config = get_config()
    ffmpeg_location = config.get(CONFIG_DB, 'ffmpeg_location')
    ffprobe_location = config.get(CONFIG_DB, 'ffprobe_location')

    if not (ffmpeg_location or ffprobe_location):
        print("FFMPEG and FFPROBE locations not set. Please enter the path to the bin folder. (e.g. C:\\Windows\\ffmpeg\\bin))")

        while not ((os.path.isfile(ffmpeg_location) or os.path.isfile(ffprobe_location))):

            # "C:\Windows\ffmpeg\bin" for windows in this case

            ffmpeg_bin_location = input(
                'Enter the path: ').strip().replace('"', '')

            ffmpeg_location = os.path.join(ffmpeg_bin_location, 'ffmpeg.exe')
            ffprobe_location = os.path.join(ffmpeg_bin_location, 'ffprobe.exe')

            if not ((os.path.isfile(ffmpeg_location) or os.path.isfile(ffprobe_location))):
                print("Invalid ffmpeg or ffprobe location. Please try again.")
            else:
                try:
                    subprocess.check_output([ffmpeg_location, '-version'])
                    print("ffmpeg location set to: " + ffmpeg_location)
                    print("ffprobe location set to: " + ffprobe_location)
                    set_config(ffmpeg_location, ffprobe_location)
                except subprocess.CalledProcessError:
                    print("Invalid ffmpeg bin folder. Please try again.")

    return ffmpeg_location, ffprobe_location


def get_downloads_folder():
    if os.name == 'nt':
        sub_key = r'SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Explorer\\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location


if __name__ == '__main__':

    print('yt-dlp helper v1.0.0 ' + '\n' + 'yt-dlp version: ' +
          yt_dlp.version.__version__ + '\n' + 'Python version: ' + sys.version + '\n')

    ffmpeg_location, ffprobe_location = get_locations()

    main_options = {
        'ffmpeg_location': ffmpeg_location,
        'ffmprobe_location': ffprobe_location,
        'outtmpl': get_downloads_folder() + '/%(title)s.%(ext)s',
    }

    link = input("Enter the link: ")

    file_type = input("Enter the file type: ")

    if file_type == "mp3":
        type_options = {
            'format': 'bestaudio/best',
            'writethumbnail': True,
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
                    'preferredquality': '192'},
                {'key': 'FFmpegMetadata', 'add_metadata': 'True'},
                {'key': 'EmbedThumbnail', 'already_have_thumbnail': False, }

            ],

        }
    elif file_type == "mp4":
        type_options = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }
    else:
        print("Error in params")
        exit()
    with yt_dlp.YoutubeDL({**main_options, **type_options}) as ydl:
        ydl.download(link)
