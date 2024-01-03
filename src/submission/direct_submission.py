import requests

from submission.submission import Submission, DownloadException


class DirectSubmission(Submission):

    def __init__(self, submission_id, title, link, community_name, url, user_agent):
        super().__init__(submission_id, title, link, community_name, url)
        self._user_agent = user_agent

    def save(self, folder, filename_suffix=''):
        try:
            r = requests.get(self.url(), headers={'user-agent': self._user_agent}, timeout=10)
            r.raise_for_status()

            content_type = r.headers['content-type']
            if content_type.split('/')[0] not in ['image', 'video']:
                raise DownloadException('Submission is not a media file. Content-Type: ' + content_type)

            filename = self.filename(folder, filename_suffix)
            filename = self.content_type_extension(filename, content_type)
            filename.parent.mkdir(parents=True, exist_ok=True)
            filename.unlink(missing_ok=True)
            filename.touch()

            with filename.open('wb') as f:
                for chunk in r.iter_content(chunk_size=128):
                    f.write(chunk)

        except requests.exceptions.RequestException as exception:
            raise DownloadException(exception)
