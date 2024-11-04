from submission.direct_submission import DirectSubmission
from submission.gfycat_submission import GfycatSubmission
from submission.imgur_submission import ImgurSubmission
from submission.redgif_submission import RedgifSubmission
from submission.tumblr_submission import TumblrSubmission


class LemmySubmissions:
    def __init__(self, lemmy_posts, imgur, redgif, output, user_agent):
        self._imgur = imgur
        self._redgif = redgif
        self._output = output
        self._user_agent = user_agent
        self._lemmy_submissions = [self._submission(s) for s in lemmy_posts]

    def submissions(self):
        return self._lemmy_submissions

    def _submission(self, lemmy_post):
        submission_id = str(lemmy_post.post.id)
        title = lemmy_post.post.name
        link = lemmy_post.post.ap_id
        community_name = lemmy_post.community.title
        url = lemmy_post.post.url

        if self._direct_image_link(url):
            return DirectSubmission(submission_id, title, link, community_name, url, self._user_agent)
        elif 'imgur' in url:
            return ImgurSubmission(submission_id, title, link, community_name, url, self._user_agent, self._imgur)
        elif 'gfycat' in url:
            return GfycatSubmission(submission_id, title, link, community_name, url, self._user_agent)
        elif 'tumblr' in url:
            return TumblrSubmission(submission_id, title, link, community_name, url, None)
        elif 'redgif' in url:
            return RedgifSubmission(submission_id, title, link, community_name, url, self._redgif)
        else:
            return DirectSubmission(submission_id, title, link, community_name, url, self._user_agent)

    def _direct_image_link(self, submission_url):
        img_ext = (".jpg", ".jpeg", ".gif")
        return submission_url.endswith(img_ext)
