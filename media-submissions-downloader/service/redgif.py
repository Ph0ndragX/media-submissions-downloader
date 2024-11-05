import requests


class Redgif:

    def __init__(self):
        self._token = None
        self._sess = None

    def get_temporary_token(self):
        self._sess = requests.Session()
        r = self._sess.get("https://api.redgifs.com/v2/auth/temporary")
        r.raise_for_status()
        self._token = r.json()["token"]

    def get_gif_info(self, gif_id):
        if self._token is None:
            self.get_temporary_token()

        r = self._sess.get(f"https://api.redgifs.com/v2/gifs/{gif_id}", headers={"Authorization": f"Bearer {self._token}"})
        r.raise_for_status()
        return r.json()

    def get_gif(self, url):
        return self._sess.get(url, headers={"Authorization": f"Bearer {self._token}"})
