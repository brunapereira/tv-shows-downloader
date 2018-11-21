import x1337

class TvShowsDownloader():
    def run(self):
        TV_SHOW = 'Greys Anatomy'
        VERSION = 'S14E05'

        x1337.download(TV_SHOW, VERSION)

if __name__ == '__main__':
    TvShowsDownloader().run()
