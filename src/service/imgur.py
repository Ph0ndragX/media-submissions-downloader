import requests


class ImgurException(Exception):
    pass


class Imgur:
    def __init__(self, imgur_credentials):
        self._imgur_credentials = imgur_credentials

    def get_media_links(self, imgur_hash):
        try:
            album = self._get_album_media_links(imgur_hash)
            return [img['link'] for img in album['images']]
        except requests.exceptions.RequestException:
            try:
                image = self._get_image_media_link(imgur_hash)
                return image['link']
            except requests.exceptions.RequestException as exception:
                raise ImgurException(exception)

    def _get_album_media_links(self, album_hash):
        album = self._request('https://api.imgur.com/3/album/' + album_hash)
        return album.json()['data']

    def _get_image_media_link(self, image_hash):
        image = self._request('https://api.imgur.com/3/image/' + image_hash)
        return image.json()['data']

    def _request(self, url):
        headers = {'Authorization': 'Client-ID ' + self._imgur_credentials['client_id']}
        r = requests.get(url, headers=headers)
        return r.json()
