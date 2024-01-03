import re
import urllib.parse

import requests

from submission.direct_submission import DirectSubmission
from submission.submission import Submission, DownloadException


class GfycatSubmission(Submission):

    def __init__(self, submission_id, title, link, community_name, url, user_agent):
        super().__init__(submission_id, title, link, community_name, url)
        self._user_agent = user_agent

    def save(self, folder):
        direct_submission = DirectSubmission(self._submission_id(), self.title(), self.link(), self.community_name(), self._get_gfycat_submission_url(), self._user_agent)
        direct_submission.save(folder)

    def _get_gfycat_submission_url(self):
        result = re.search('/([a-zA-Z0-9]+)[.a-zA-Z0-9\\-]*$', urllib.parse.urlparse(self.url()).path)
        if result is None:
            raise DownloadException(
                'Could not retrieve gfycat name from url: ' + urllib.parse.urlparse((self.url())).path
            )
        try:
            try:
                r = requests.get('https://api.gfycat.com/v1/gfycats/' + result.group(1).lower(), timeout=10)
                r.raise_for_status()
            except requests.exceptions.RequestException as exception:
                r = requests.get('https://api.redgifs.com/v1/gfycats/' + result.group(1).lower(), timeout=10)
                r.raise_for_status()

            json = r.json()
            if 'gfyItem' not in json:
                raise DownloadException('Gyfcat api error. Response: ' + r.text)
            json = json['gfyItem']

            if 'mp4Url' not in json:
                raise DownloadException('Gyfcat api error. Response: ' + r.text)

            return json['mp4Url']

        except requests.exceptions.RequestException as exception:
            raise DownloadException(exception)
        except ValueError as exception:
            raise DownloadException(exception)
