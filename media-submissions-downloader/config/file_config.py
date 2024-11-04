import configparser


class FileConfig:

    def __init__(self, filename):
        self._config = configparser.ConfigParser()
        self._config.read(filename)
        
        self._reddits_configs = []
        self._lemmys_configs = []
        self._imgur_config = {'client_id': self._config['imgur']['client_id']}
        self._user_agent = self._config['default']['user_agent'] 
        
        for social in [s.strip() for s in self._config['default']['socials'].split(",")]:
            social_config = self._config[social]
            social_type = social_config["type"]
            if social_type == 'reddit':
                self._reddits_configs.append(self._reddit_config(social, social_config))
            elif social_type == "lemmy":
                self._lemmys_configs.append(self._lemmy_config(social, social_config))

    def user_agent(self):
        return self._user_agent

    def reddits_configs(self):
        return self._reddits_configs

    def lemmys_configs(self):
        return self._lemmys_configs

    def imgur_config(self):
        return self._imgur_config

    def _reddit_config(self, name, social_config):
        return {
            'name': name,
            'output': social_config['output'],
            'client_id': social_config['client_id'],
            'client_secret': social_config['client_secret'],
            'username': social_config['username'],
            'password': social_config['password'],
            'user_agent': self._user_agent
        }

    def _lemmy_config(self, name, social_config):
        return {
            "name": name,
            "url": social_config["url"],
            "output": social_config["output"],
            "username": social_config["username"],
            "password": social_config["password"],
        }
