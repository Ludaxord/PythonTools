import time

import youtube_dl
from moviepy.editor import *
from os import listdir
from os.path import isfile, join


class YoutubeDownloader:

    def get_videos_and_convert(self, urls, file_path, audio_path):
        for url in urls:
            print(f"starting download... {url}")
            successful = False
            while not successful:
                try:
                    self.get_video_with_youtube_dl(url, file_path)
                    successful = True
                except Exception as e:
                    print(f"problem with downloading taking sleep, {e}")
                    time.sleep(1000)

        files = self.get_videos_list_from_dir(file_path)
        for file in files:
            self.convert_mp4_to_mp3(f"{file_path}/{file}", audio_path)

    def convert_mp4_to_mp3(self, movie_path, audio_path):
        video = VideoFileClip(movie_path)
        video.audio.write_audiofile(audio_path)

    def get_video_with_youtube_dl(self, url, file_path, urls=None):
        ydl_opts = {
            'outtmpl': os.path.join(file_path, '%(title)s-%(id)s.%(ext)s'),
        }
        if urls is None:
            urls = [url]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

    def get_videos_list_from_dir(self, path):
        files = [f for f in listdir(path) if isfile(join(path, f))]
        return files

# Usage
# urls = []
# main_path = ""
# youtube_downloader = YoutubeDownloader()
# youtube_downloader.get_video_with_youtube_dl(None, f"{main_path}/videos", urls)
