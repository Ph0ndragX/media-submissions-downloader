import traceback

from submission.lemmy_submissions import LemmySubmissions
from submission.reddit_submissions import RedditSubmissions
from submission.submission import DownloadException


class MediaSubmissionDownloader:

    def __init__(self, reddits, lemmys, imgur, redgif, user_agent):
        self._reddits = reddits
        self._lemmys = lemmys
        self._imgur = imgur
        self._redgif = redgif
        self._user_agent = user_agent

    def run(self):
        for reddit in self._reddits:
            print(f"Processing social: {reddit.name()}")
            self._process_reddit(reddit)
            print(f"Finished social: {reddit.name()}")

        for lemmy in self._lemmys:
            print(f"Processing social: {lemmy.name()}")
            self._process_lemmy(lemmy)
            print(f"Finished: {lemmy.name()}")

    def _process_reddit(self, reddit):
        print(f"Reddit user: {reddit.username()}")
        submissions = RedditSubmissions(reddit.submissions(), self._imgur, self._redgif, reddit.output(), self._user_agent).submissions()
        print(f"Total submission(s): {len(submissions)}")
        output = reddit.output()
        not_downloaded_submissions = [s for s in submissions if not s.is_downloaded(output)]
        print(f"Not downloaded submission(s): {len(not_downloaded_submissions)}")
        print(f"Downloading to '{output}'")

        for s in not_downloaded_submissions:
            try:
                s.save(output)
                print(self._format_submission_display(s, "Downloaded"))
            except DownloadException:
                print(self._format_submission_display(s, f"Exception occurred: \n{traceback.format_exc()}"))

    def _process_lemmy(self, lemmy):
        print(f"Lemmy user: {lemmy.username()}")
        submissions = LemmySubmissions(lemmy.submissions(), self._imgur, self._redgif, lemmy.output(), self._user_agent).submissions()
        print(f"Total submission(s): {len(submissions)}")
        output = lemmy.output()
        not_downloaded_submissions = [s for s in submissions if not s.is_downloaded(output)]
        print(f"Not downloaded submission(s): {len(not_downloaded_submissions)}")
        print(f"Downloading to '{output}'")

        for s in not_downloaded_submissions:
            try:
                s.save(output)
                print(self._format_submission_display(s, "Downloaded"))
            except DownloadException:
                print(self._format_submission_display(s, f"Exception occurred: \n{traceback.format_exc()}"))

    def _format_submission_display(self, submission, message=''):
        return f"{submission.title()} | {submission.community_name()} | {submission.link()} | {message}"
