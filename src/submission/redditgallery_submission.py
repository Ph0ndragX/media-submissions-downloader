from submission.direct_submission import DirectSubmission
from submission.submission import Submission
import mimetypes


class RedditGallery(Submission):

    def __init__(self, user_agent, reddit_submission):
        super().__init__(reddit_submission)
        self._user_agent = user_agent
        self._reddit_submission = reddit_submission

    def save(self, folder):
        images = self._get_gallery_images_urls()
        for idx, media_url in enumerate(images):
            direct_submission = DirectSubmission(self._user_agent, self._reddit_submission, media_url)
            direct_submission.save(folder, '' if idx == 0 else ' ' + str(idx + 1))

    def _get_gallery_images_urls(self):
        return [
            ("http://i.redd.it/" + metadata['id'] + RedditGallery._guess_extension(metadata['m']))
            for (media_id, metadata) in self._reddit_submission.media_metadata.items()
        ]

    @staticmethod
    def _guess_extension(content_type):
        if content_type == "image/jpg":
            content_type = "image/jpeg"

        ext = mimetypes.guess_extension(content_type)
        if ext in ['.jpe', '.jpeg']:
            ext = '.jpg'
        return ext
