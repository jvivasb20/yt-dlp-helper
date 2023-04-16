import configparser
import os
import winreg

import yt_dlp

CONFIG_FILE = 'config.ini'
FFMPEG_LOCATION = ''
FFPROBE_LOCATION = ''

""" def get_config():

    config = configparser.ConfigParser()

    ffmpeg_location = config.get('FFMPEG', 'ffmpeg_location')
    ffprobe_location = config.get('FFPROBE', 'ffprobe_location')

    if not ffmpeg_location or not ffprobe_location:
        ffmpeg_location = input('Enter the path to ffmpeg: ')
        ffprobe_location = input('Enter the path to ffprobe: ')
        set_config(ffmpeg_location, ffprobe_location)
    return configparser.ConfigParser()

def set_config(ffmpeg_location, ffprobe_location):
    config = get_config()
    config.set('FFMPEG', 'ffmpeg_location', ffmpeg_location)
    config.set('FFPROBE', 'ffprobe_location', ffprobe_location)
    with open(CONFIG_FILE, 'w') as f:
        config.write(f) """


def get_downloads_folder():
    if os.name == 'nt':
        sub_key = r'SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Explorer\\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location


if __name__ == '__main__':

    link = input("Enter the link: ")

    file_type = input("Enter the file type: ")

    options = {
        'ffmpeg_location': 'C:\\Windows\\ffmpeg\\bin\\ffmpeg.exe',
        'ffmprobe_location': 'C:\\Windows\\ffmpeg\\bin\\ffprobe.exe',
        'outtmpl': get_downloads_folder() + '/%(title)s.%(ext)s',
    }

    if file_type == "mp3":

        options['format'] = 'bestaudio/best'
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    elif file_type == "mp4":
        options['format'] = 'bestvideo+bestaudio/best'
        options['merge_output_format'] = 'mp4'

    else:
        print("Error in params")
        exit()

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(link)
