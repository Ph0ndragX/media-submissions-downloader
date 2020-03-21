from submission.submission import Submission


class TumblrSubmission(Submission):

    def __init__(self, tumblr, reddit_submission):
        super().__init__(reddit_submission)
        self._tumblr = tumblr
        self._reddit_submission = reddit_submission

    def save(self, folder):
        raise NotImplementedError()
