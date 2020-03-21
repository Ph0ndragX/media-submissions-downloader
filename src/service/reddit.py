import praw


class Reddit:

    def __init__(self, reddit_credentials):
        self.reddit = praw.Reddit(
            client_id=reddit_credentials['client_id'],
            client_secret=reddit_credentials['client_secret'],
            username=reddit_credentials['username'],
            password=reddit_credentials['password'],
            user_agent=reddit_credentials['user_agent']
        )
        self._cached_saved_submissions = []

    def user(self):
        return self.reddit.user.me()

    def saved_link_submissions(self):
        return [submission for submission in self.saved_submissions() if submission.name[:2] == 't3']

    def saved_submissions(self):
        if len(self._cached_saved_submissions) == 0:
            self._cached_saved_submissions = \
                list(self.reddit.user.me().saved(limit=None, params={'sort': 'new', 'time': 'all'}))
        return self._cached_saved_submissions
