import re
import urllib.parse

from service import imgur
from submission.direct_submission import DirectSubmission
from submission.submission import Submission, DownloadException


class ImgurSubmission(Submission):

    def __init__(self, imgur, reddit_submission):
        super().__init__(reddit_submission)
        self._imgur = imgur
        self._reddit_submission = reddit_submission

    def save(self, folder):
        for idx, media_url in enumerate(self._get_imgur_submission_urls()):
            direct_submission = DirectSubmission(self._reddit_submission, media_url)
            direct_submission.save(folder, '' if idx == 0 else ' ' + str(idx + 1))

    def _get_imgur_submission_urls(self):
        try:
            return self._imgur.get_media_links(self._extract_imgur_hash(self._reddit_submission.url))
        except imgur.ImgurException as exception:
            raise DownloadException(exception)

    @staticmethod
    def _extract_imgur_hash(url):
        path = urllib.parse.urlparse(url).path
        result = re.search('([a-zA-Z0-9]+)', path.split('/')[-1])
        if result is None:
            raise DownloadException('No imgur id found for url: ' + url)
        return result.group(1)
