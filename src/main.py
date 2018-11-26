import logging
import os
import glob

from videos import aria2c
from videos.client import x1337
from subtitles.client import subdb
from shows.client.thetvdb import TheTvDb
from repository.client import redis
from models.File import File

BASE_TV_SHOWS_DIR = 'tv-shows/'

class TvShowsDownloader():
    def __init__(self):
        logging.basicConfig(
            filename='tv-shows-downloader.log',
            level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d %(levelname)s Module: %(module)s - Function: %(funcName)s: Message: %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S")

    def run(self):
        # Save shows in DB
        TheTvDb().fetch_favorite_shows()

        # Retrieve shows from DB
        shows = redis.get_all_tv_shows()

        for tv_show in shows:
            # Download video
            magnet_link = x1337.fetch_magnet_link(tv_show.name, tv_show.episode)

            # Create dir
            directory = self.create_directory(tv_show)

            # Download Video
            aria2c.download_at(directory, magnet_link)

            # Move video to root folder
            video_file = self.move_video(directory)

            # Download subtitle
            subdb.fetch_subtitle(video_file)

    def create_directory(self, tv_show):
        dir_name = '{0}{1}-{2}/'.format(BASE_TV_SHOWS_DIR, tv_show.name, tv_show.episode)

        try:
            os.makedirs(dir_name)
            print("Directory", dir_name, "Created")
        except FileExistsError:
            print("Directory", dir_name,  "already exists")

        return dir_name

    def move_video(self, directory):
        directories = [directory + '/**/*.' + extension for extension in ['mkv', 'mp4', 'avi']]
        paths = []

        for dir_with_extension in directories:
            paths.extend(glob.glob(dir_with_extension, recursive=True))

        video_file = File(paths[-1])
        
        return video_file.move_to(directory)

if __name__ == '__main__':
    TvShowsDownloader().run()
