from videos.client import x1337
from subtitles.client import subdb
from shows.client import thetvdb
from repository.client import redis

class TvShowsDownloader():
    def run(self):
        shows = thetvdb.TheTvDb()
        shows.login()
        shows.get_info_from_favorites()

        for tv_show in redis.get_all_tv_shows():
            # Download video
            video_file = x1337.fetch_video(tv_show.name, tv_show.episode)

            # Download subtitle
            subdb.fetch_subtitle(video_file)


if __name__ == '__main__':
    TvShowsDownloader().run()
