import redgifs


class Redgif:

    def __init__(self):
        self._api = redgifs.API()
        self._api.login()

    def get_gif_info(self, gif_id):
        return self._api.get_gif(gif_id)

    def get_gif(self, url, out):
        self._api.download(url, out)
