import concurrent
from concurrent.futures.thread import ThreadPoolExecutor

from submission.direct_submission import DirectSubmission
from submission.gfycat_submission import GfycatSubmission
from submission.imgur_submission import ImgurSubmission
from submission.redditgallery_submission import RedditGallery
from submission.redgif_submission import RedgifSubmission
from submission.tumblr_submission import TumblrSubmission


class MediaSubmissions:
    def __init__(self, config, reddit, imgur):
        self._config = config
        self._reddit = reddit
        self._imgur = imgur

    def user(self):
        return self._reddit.user()

    def save(self, on_downloaded, on_error, skip_downloaded=True):
        submissions_to_download = \
            [sub for sub in self.submissions() if not (skip_downloaded and sub.is_downloaded(self._config.save_dir()))]

        with ThreadPoolExecutor() as e:
            try:
                future_to_submission = {
                    e.submit(lambda x: x.save(self._config.save_dir()), sub): sub
                    for sub in submissions_to_download
                }
                for idx, future in enumerate(concurrent.futures.as_completed(future_to_submission), start=1):
                    submission = future_to_submission[future]
                    try:
                        future.result()
                        on_downloaded(idx, submission)
                    except Exception as e:
                        on_error(idx, submission, e)
            except KeyboardInterrupt:
                for future in future_to_submission:
                    future.cancel()
                print('[!] Stopping execution. Waiting for remaining threads to finish execution.')

    def submissions(self):
        return [self._submission(submission) for submission in self._reddit.saved_link_submissions()]

    def downloaded_submissions(self):
        return [submission for submission in self.submissions() if submission.is_downloaded(self._config.save_dir())]

    def _submission(self, reddit_submission):
        if MediaSubmissions.direct_image_link(reddit_submission):
            return DirectSubmission(self._config.user_agent(), reddit_submission, reddit_submission.url)
        elif 'imgur' in reddit_submission.url:
            return ImgurSubmission(self._config.user_agent(), self._imgur, reddit_submission)
        elif 'gfycat' in reddit_submission.url:
            return GfycatSubmission(self._config.user_agent(), reddit_submission)
        elif 'tumblr' in reddit_submission.url:
            return TumblrSubmission(None, reddit_submission)
        elif 'redgifs' in reddit_submission.url:
            return RedgifSubmission(self._config.user_agent(), reddit_submission)
        elif 'reddit.com/gallery' in reddit_submission.url:
            return RedditGallery(self._config.user_agent(), reddit_submission)
        else:
            return DirectSubmission(self._config.user_agent(), reddit_submission, reddit_submission.url)

    @staticmethod
    def direct_image_link(reddit_submission):
        img_ext = (".jpg", ".jpeg", ".gif")
        return reddit_submission.url.endswith(img_ext)
