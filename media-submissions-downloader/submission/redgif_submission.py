import urllib.parse

import requests

from submission.submission import Submission, DownloadException


class RedgifSubmission(Submission):

    def __init__(self, submission_id, title, link, community_name, url, redgif):
        super().__init__(submission_id, title, link, community_name, url)
        self._redgif = redgif

    def save(self, folder, filename_suffix=''):
        try:
            gif_info = self._redgif.get_gif_info(self._extract_id(self.url()))
            hd_url = gif_info["gif"]["urls"]["hd"]
            gif = self._redgif.get_gif(hd_url)

            extension = self._extract_extension(hd_url)
            filename = self.filename(folder, filename_suffix).with_suffix(extension)
            filename.parent.mkdir(parents=True, exist_ok=True)
            filename.unlink(missing_ok=True)
            filename.touch()

            with filename.open('wb') as f:
                for chunk in gif.iter_content(chunk_size=128):
                    f.write(chunk)

        except requests.exceptions.RequestException as exception:
            raise DownloadException(f"Got response {exception.response.status_code} with body: {exception.response.text}")

    def _extract_id(self, url):
        extracted = None
        parts = urllib.parse.urlparse(url).path.split("/")
        parts.reverse()
        for p in parts:
            if p == '':
                continue
            else:
                extracted = p
                break

        if extracted is None or extracted.strip() == '':
            raise Exception("Failed to extract redgif id from URL: " + url)
        return extracted

    def _extract_extension(self, url):
        last_fragment = urllib.parse.urlparse(url).path.split("/")[-1]
        extension = last_fragment.split(".")[-1]
        return f".{extension}"
