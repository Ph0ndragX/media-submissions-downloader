import concurrent
from concurrent.futures import ThreadPoolExecutor

import praw.exceptions
import prawcore.exceptions

from submission.reddit_submissions import RedditSubmissions


class MediaSubmissionDownloader:

    def __init__(self, reddits, imgur, redgif, user_agent):
        self._reddits = reddits
        self._imgur = imgur
        self._redgif = redgif
        self._user_agent = user_agent

    def run(self):
        for reddit in self._reddits:
            try:
                print(f"Processing social: {reddit.name()}")
                self._process_reddit(reddit)
            except prawcore.exceptions.PrawcoreException as e:
                print(f"Failed to process: {str(e)}")

    def _process_reddit(self, reddit):
        print(f"Reddit user: {reddit.username()}")
        submissions = RedditSubmissions(reddit.submissions(), self._imgur, self._redgif, reddit.output(), self._user_agent).submissions()
        print(f"Total submission(s): {len(submissions)}")
        output = reddit.output()
        not_downloaded_submissions = [s for s in submissions if not s.is_downloaded(output)]
        print(f"Not downloaded submission(s): {len(not_downloaded_submissions)}")
        print(f"Downloading to '{output}'")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_submission = {executor.submit(s.save, output): s for s in not_downloaded_submissions}
            for future in concurrent.futures.as_completed(future_to_submission):
                submission = future_to_submission[future]
                try:
                    data = future.result()
                    print(self._format_submission_display(submission, "Downloaded"))
                except Exception as e:
                    print(self._format_submission_display(submission, str(e)))

    def _format_submission_display(self, submission, message=''):
        fmt = "{:<32.32} | {:^23} "
        title = submission.title() if len(submission.title()) <= 32 else submission.title()[:(32 - 3)] + '...'
        formatted = fmt.format(title, submission.shortlink())
        return formatted if message == '' else formatted + ' | ' + message
