import pathlib


class Config:

    def __init__(self, arg_config, file_config):
        self._arg_config = arg_config
        self._file_config = file_config

    def reddit_credentials(self):
        credentials = self._file_config.reddit_credentials()
        credentials.update(self._arg_config.reddit_credentials())
        return credentials

    def imgur_credentials(self):
        credentials = self._file_config.imgur_credentials()
        credentials.update(self._arg_config.imgur_credentials())
        return credentials

    def save_dir(self):
        save_dir = self._arg_config.save_dir()
        if save_dir is None:
            save_dir = self._file_config.save_dir()
        if save_dir is None:
            save_dir = pathlib.Path('output')
        return save_dir

    def display(self):
        return self._arg_config.display() or self._file_config.display()

    def user_agent(self):
        user_agent = self._arg_config.user_agent()
        if user_agent is None:
            user_agent = self._file_config.user_agent()
        if user_agent is None:
            user_agent = 'custom'
        return user_agent
