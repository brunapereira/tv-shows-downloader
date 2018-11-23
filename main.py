from videos.client import x1337
from subtitles.client import subdb
from shows.client import thetvdb

class TvShowsDownloader():
    def run(self):
        TV_SHOW = 'Greys Anatomy'
        VERSION = 'S14E05'

        shows = thetvdb.TheTvDb()
        shows.login()
        shows.get_info_from_favorites()

        # Get TV Shows from Redis
        # Check if files exist
        # Download video and subtitle

        # Download video
        video_file = x1337.fetch_video(TV_SHOW, VERSION)

        # Download subtitle
        subdb.fetch_subtitle(video_file)


if __name__ == '__main__':
    TvShowsDownloader().run()
