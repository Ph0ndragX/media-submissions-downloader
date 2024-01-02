import mimetypes
import re
from abc import ABC, abstractmethod


FILENAME_LENGTH_LIMIT = 100


class DownloadException(Exception):
    pass


class Submission(ABC):

    def __init__(self, reddit_submission):
        self._reddit_submission = reddit_submission

    @abstractmethod
    def save(self, folder):
        pass

    def title(self):
        return self._reddit_submission.title

    def shortlink(self):
        return self._reddit_submission.shortlink

    def subreddit_name(self):
        return self._reddit_submission.subreddit.display_name

    def filename(self, folder, filename_suffix=''):
        subreddit = Submission._normalize_name(self._reddit_submission.subreddit.display_name)
        title = Submission._normalize_name(self._reddit_submission.id + "_" + self._reddit_submission.title)
        if len(title) > FILENAME_LENGTH_LIMIT:
            title = title[:FILENAME_LENGTH_LIMIT]
        title += filename_suffix
        return folder.joinpath(subreddit, title)

    def is_downloaded(self, folder):
        return self._file_exists_ignoring_extension(self.filename(folder))

    @staticmethod
    def content_type_extension(filename, content_type):
        return filename.with_suffix(Submission._guess_extension(content_type))

    @staticmethod
    def _normalize_name(filename):
        return re.sub('[^a-zA-Z0-9!,\s\(\)\[\]\-]', '_', filename)

    @staticmethod
    def _guess_extension(content_type):
        if content_type == "image/jpg":
            content_type = "image/jpeg"

        ext = mimetypes.guess_extension(content_type)
        if ext in ['.jpe', '.jpeg']:
            ext = '.jpg'
        return ext

    @staticmethod
    def _file_exists_ignoring_extension(filename):
        if not filename.parent.is_dir():
            return False

        for p in filename.parent.iterdir():
            if p.stem == filename.stem:
                return True
        return False
