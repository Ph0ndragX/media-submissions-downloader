import re
import urllib.parse

import requests

from submission.direct_submission import DirectSubmission
from submission.submission import Submission, DownloadException


class GfycatSubmission(Submission):

    def __init__(self, user_agent, reddit_submission):
        super().__init__(reddit_submission)
        self._user_agent = user_agent
        self._reddit_submission = reddit_submission

    def save(self, folder):
        direct_submission = DirectSubmission(self._user_agent, self._reddit_submission, self._get_gfycat_submission_url())
        direct_submission.save(folder)

    def _get_gfycat_submission_url(self):
        result = re.search('/([a-zA-Z0-9]+)[.a-zA-Z0-9\\-]*$', urllib.parse.urlparse(self._reddit_submission.url).path)
        if result is None:
            raise DownloadException(
                'Could not retrieve gfycat name from url: ' + urllib.parse.urlparse(self._reddit_submission.url).path
            )
        try:
            try:
                r = requests.get('https://api.gfycat.com/v1/gfycats/' + result.group(1))
                r.raise_for_status()
            except requests.exceptions.RequestException as exception:
                r = requests.get('https://api.redgifs.com/v1/gfycats/' + result.group(1))
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
