import pathlib

import praw


class Reddit:

    def __init__(self, config):
        self._name = config['name']
        self.reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            username=config['username'],
            password=config['password'],
            user_agent=config['user_agent']
        )
        self._output = config['output']
        self._cached_saved_submissions = []

    def name(self):
        return self._name

    def output(self):
        return pathlib.Path(self._output)

    def username(self):
        return self.reddit.user.me().name

    def submissions(self):
        if len(self._cached_saved_submissions) == 0:
            self._cached_saved_submissions = self._saved_media__submissions()
        return self._cached_saved_submissions

    def _saved_media__submissions(self):
        return [
            submission for submission in
            list(self.reddit.user.me().saved(limit=None, params={'sort': 'new', 'time': 'all'}))
            if submission.name[:2] == 't3'
        ]
