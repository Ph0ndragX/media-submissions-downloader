from submission.submission import Submission


class TumblrSubmission(Submission):

    def __init__(self, submission_id, title, link, community_name, url, tumblr):
        super().__init__(submission_id, title, link, community_name, url)
        self._tumblr = tumblr

    def save(self, folder):
        raise NotImplementedError()
