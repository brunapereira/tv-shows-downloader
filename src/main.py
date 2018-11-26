from videos.client import x1337
from subtitles.client import subdb
from shows.client.thetvdb import TheTvDb
from repository.client import redis
import logging

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
            video_file = x1337.fetch_video(tv_show.name, tv_show.episode)

            # Download subtitle
            subdb.fetch_subtitle(video_file)

if __name__ == '__main__':
    TvShowsDownloader().run()
