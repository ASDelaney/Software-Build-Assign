from typing import Any, Optional
import yaml
import requests
import matplotlib.pyplot as plt


class Analysis():

    def __init__(self, analysis_config: str) -> None:
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        self.config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            self.config.update(this_config)

        self.dataset = None

    def load_data(self) -> None:
        try:
            # Loading NYT API key from YAML file
            with open(self.config['secrets_file']) as f:
                nyt_secrets = yaml.safe_load(f)

            # Retrieving data from NYT API
            api_key = nyt_secrets['API_key']
            nyt_url = 'https://api.nytimes.com/svc/archive/v1/2019/1.json'
            params = {'api-key': api_key}
            self.dataset = requests.get(nyt_url, params=params).json()

        except Exception as e:
            print(f"Error loading data: {e}")
            raise