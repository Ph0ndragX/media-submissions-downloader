import argparse
import pathlib


class ArgConfig:

    def __init__(self, banner):
        parser = argparse.ArgumentParser(description=banner)
        parser.add_argument('-o', '--output-dir',
                            help='directory where to save downloaded submissions')
        parser.add_argument('-c', '--config-filename', default='./config.ini',
                            help='config filename')
        parser.add_argument('-d', '--display', action='store_true',
                            help='display submissions list')
        parser.add_argument('-u', '--user-agent', default="custom",
                            help='user-agent')

        parser.add_argument('--reddit-client-id',
                            help='reddit client id')
        parser.add_argument('--reddit-client-secret',
                            help='reddit client secret')
        parser.add_argument('--reddit-username',
                            help='reddit username')
        parser.add_argument('--reddit-password',
                            help='reddit password')

        parser.add_argument('--imgur-client-id',
                            help='imgur client id')

        self._arguments = parser.parse_args()

    def reddit_credentials(self):
        credentials = {}
        if self._arguments.reddit_client_id is not None:
            credentials['client_id'] = self._arguments.reddit_client_id

        if self._arguments.reddit_client_secret is not None:
            credentials['client_secret'] = self._arguments.reddit_client_secret

        if self.user_agent() is not None:
            credentials['user_agent'] = self.user_agent()

        if self._arguments.reddit_username is not None:
            credentials['username'] = self._arguments.reddit_username

        if self._arguments.reddit_password is not None:
            credentials['password'] = self._arguments.reddit_password
        return credentials

    def imgur_credentials(self):
        credentials = {}
        if self._arguments.imgur_client_id is not None:
            credentials['client_id'] = self._arguments.imgur_client_id
        return credentials

    def save_dir(self):
        if self._arguments.output_dir is None:
            return None
        return pathlib.Path(self._arguments.output_dir)

    def display(self):
        return self._arguments.display

    def config_file(self):
        return pathlib.Path(self._arguments.config_filename)

    def user_agent(self):
        return self._arguments.user_agent
