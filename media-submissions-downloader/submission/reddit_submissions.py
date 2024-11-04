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
        submission_id = reddit_submission.id
        title = reddit_submission.title
        link = reddit_submission.shortlink
        community_name = reddit_submission.subreddit.display_name
        url = reddit_submission.url

        if self._direct_image_link(url):
            return DirectSubmission(submission_id, title, link, community_name, url, self._user_agent)
        elif 'imgur' in url:
            return ImgurSubmission(submission_id, title, link, community_name, url, self._user_agent, self._imgur)
        elif 'gfycat' in url:
            return GfycatSubmission(submission_id, title, link, community_name, url, self._user_agent)
        elif 'tumblr' in url:
            return TumblrSubmission(submission_id, title, link, community_name, url, None)
        elif 'reddit.com/gallery' in url:
            return RedditGallery(submission_id, title, link, community_name, url, self._user_agent, reddit_submission)
        elif 'redgif' in url:
            return RedgifSubmission(submission_id, title, link, community_name, url, self._redgif)
        else:
            return DirectSubmission(submission_id, title, link, community_name, url, self._user_agent)

    def _direct_image_link(self, submission_url):
        img_ext = (".jpg", ".jpeg", ".gif")
        return submission_url.endswith(img_ext)
