from videos.client import x1337
from subtitles.client import subdb

class TvShowsDownloader():
    def run(self):
        TV_SHOW = 'Greys Anatomy'
        VERSION = 'S14E05'

        # Download video
        video_file = x1337.fetch_video(TV_SHOW, VERSION)

        # Download subtitle
        subdb.fetch_subtitle(video_file)

if __name__ == '__main__':
    TvShowsDownloader().run()
