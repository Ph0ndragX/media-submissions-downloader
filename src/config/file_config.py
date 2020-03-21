import configparser
import pathlib


class FileConfig:

    def __init__(self, filename):
        self._config = configparser.ConfigParser()
        self._config.read(filename)

    def reddit_credentials(self):
        if 'reddit' not in self._config:
            return {}

        credentials = {}
        if 'client_id' in self._config['reddit']:
            credentials['client_id'] = self._config['reddit']['client_id']

        if 'client_secret' in self._config['reddit']:
            credentials['client_secret'] = self._config['reddit']['client_secret']

        if self.user_agent() is not None:
            credentials['user_agent'] = self.user_agent()

        if 'username' in self._config['reddit']:
            credentials['username'] = self._config['reddit']['username']

        if 'password' in self._config['reddit']:
            credentials['password'] = self._config['reddit']['password']
        return credentials

    def imgur_credentials(self):
        if 'imgur' not in self._config:
            return {}

        credentials = {}
        if 'client_id' in self._config['imgur']:
            credentials['client_id'] = self._config['imgur']['client_id']
        return credentials

    def save_dir(self):
        if 'default' not in self._config or 'output_dir' not in self._config['default']:
            return None

        return pathlib.Path(self._config['default']['output_dir'])

    def display(self):
        if 'default' not in self._config:
            return None

        return self._config['default'].getboolean('display')

    def user_agent(self):
        if 'default' not in self._config or 'user_agent' not in self._config['default']:
            return None

        return self._config['default']['user_agent']
