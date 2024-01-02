from submission.direct_submission import DirectSubmission
from submission.gfycat_submission import GfycatSubmission
from submission.imgur_submission import ImgurSubmission
from submission.redditgallery_submission import RedditGallery
from submission.redgif_submission import RedgifSubmission
from submission.tumblr_submission import TumblrSubmission


class RedditSubmissions:
    def __init__(self, reddit_submissions, imgur, redgif, output, user_agent):
        self._imgur = imgur
        self._redgif = redgif
        self._output = output
        self._user_agent = user_agent
        self._reddit_submissions = [self._submission(s) for s in reddit_submissions]

    def submissions(self):
        return self._reddit_submissions

    def _submission(self, reddit_submission):
        if self._direct_image_link(reddit_submission):
            return DirectSubmission(self._user_agent, reddit_submission, reddit_submission.url)
        elif 'imgur' in reddit_submission.url:
            return ImgurSubmission(self._user_agent, self._imgur, reddit_submission)
        elif 'gfycat' in reddit_submission.url:
            return GfycatSubmission(self._user_agent, reddit_submission)
        elif 'tumblr' in reddit_submission.url:
            return TumblrSubmission(None, reddit_submission)
        elif 'reddit.com/gallery' in reddit_submission.url:
            return RedditGallery(self._user_agent, reddit_submission)
        elif 'redgif' in reddit_submission.url:
            return RedgifSubmission(self._redgif, reddit_submission)
        else:
            return DirectSubmission(self._user_agent, reddit_submission, reddit_submission.url)

    def _direct_image_link(self, reddit_submission):
        img_ext = (".jpg", ".jpeg", ".gif")
        return reddit_submission.url.endswith(img_ext)
