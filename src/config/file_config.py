import configparser


class FileConfig:

    def __init__(self, filename):
        self._config = configparser.ConfigParser()
        self._config.read(filename)
        
        self._reddits_configs = []
        self._imgur_config = {'client_id': self._config['imgur']['client_id']}
        self._user_agent = self._config['default']['user_agent'] 
        
        for social in [s.strip() for s in self._config['default']['socials'].split(",")]:
            social_config = self._config[social]
            social_type = social_config["type"]
            if social_type == 'reddit':
                self._reddits_configs.append(self._reddit_config(social, social_config))

    def user_agent(self):
        return self._user_agent

    def reddit_configs(self):
        return self._reddits_configs

    def imgur_config(self):
        return self._imgur_config

    def _reddit_config(self, name, social_config):
        return {
            'name': name,
            'output': social_config['output'],
            'client_id': social_config['client_id'],
            'client_secret': social_config['client_secret'],
            'username': self._config['reddit']['username'],
            'password': self._config['reddit']['password'],
            'user_agent': self._user_agent
        }
