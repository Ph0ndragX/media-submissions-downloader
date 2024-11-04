import pathlib

import plemmy


class Lemmy:

    def __init__(self, config):
        self._name = config['name']
        self._lemmy = plemmy.LemmyHttp(config['url'])
        self._output = config['output']
        self._cached_saved_submissions = []
        self._username = config["username"]
        self._lemmy.login(config['username'], config['password'])

    def name(self):
        return self._name

    def output(self):
        return pathlib.Path(self._output)

    def username(self):
        return plemmy.responses.GetPersonDetailsResponse(self._lemmy.get_person_details(username=self._username)).person_view.person.name

    def submissions(self):
        if len(self._cached_saved_submissions) == 0:
            self._cached_saved_submissions = self._saved_media_submissions()
        return self._cached_saved_submissions

    def _saved_media_submissions(self):
        all_posts = []

        page = 1
        while True:
            r = self._lemmy.get_posts(saved_only="true", page=page, limit=20)
            posts = plemmy.responses.GetPostsResponse(r).posts
            if len(posts) == 0:
                break
            all_posts.extend(posts)
            page += 1

        return all_posts
