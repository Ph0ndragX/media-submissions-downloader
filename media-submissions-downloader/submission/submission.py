import mimetypes
import re
from abc import ABC, abstractmethod


FILENAME_LENGTH_LIMIT = 100

mimetypes.add_type("image/webp", ".webp")

class DownloadException(Exception):
    pass


class Submission(ABC):

    def __init__(self, submission_id, title, link, community_name, url):
        self._submission_id = submission_id
        self._title = title
        self._link = link
        self._community_name = community_name
        self._url = url

    @abstractmethod
    def save(self, folder):
        pass

    def submission_id(self):
        return self._submission_id

    def community_name(self):
        return self._community_name

    def title(self):
        return self._title

    def link(self):
        return self._link

    def url(self):
        return self._url

    def filename(self, folder, filename_suffix=''):
        community_name = Submission._normalize_name(self._community_name)
        title = Submission._normalize_name(self._submission_id + "_" + self._title)
        if len(title) > FILENAME_LENGTH_LIMIT:
            title = title[:FILENAME_LENGTH_LIMIT]
        title += filename_suffix
        return folder.joinpath(community_name, title)

    def is_downloaded(self, folder):
        return self._file_exists_ignoring_extension(self.filename(folder))

    @staticmethod
    def content_type_extension(filename, content_type):
        return filename.with_suffix(Submission._guess_extension(content_type))

    @staticmethod
    def _normalize_name(filename):
        return re.sub(r"[^a-zA-Z0-9!, \[\]()-]", '_', filename).strip()

    @staticmethod
    def _guess_extension(content_type):
        if content_type == "image/jpg":
            content_type = "image/jpeg"

        ext = mimetypes.guess_extension(content_type, strict=False)
        if ext in ['.jpe', '.jpeg']:
            ext = '.jpg'

        if ext is None:
            raise Exception(f"Unable to guess extension for content type: '{content_type}'")
        return ext

    @staticmethod
    def _file_exists_ignoring_extension(filename):
        if not filename.parent.is_dir():
            return False

        for p in filename.parent.iterdir():
            if p.stem == filename.stem:
                return True
        return False
