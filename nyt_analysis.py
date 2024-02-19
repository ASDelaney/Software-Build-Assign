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

    def compute_analysis(self) -> Any:
        try:
            if self.dataset is not None:
                # Extracting word counts from the dataset
                word_counts = [article.get('word_count', 0) for article in self.dataset.get('response', {}).get('docs', [])]

                # Computing the average word count
                average_word_count = sum(word_counts) / len(word_counts) if len(word_counts) > 0 else 0

                # Visualizing word counts with a bar chart
                save_path = 'plot.png'  # Save in the current folder
                self.plot_data(word_counts, save_path)

                return average_word_count

            else:
                raise RuntimeError("Data not loaded. Call load_data() first.")
        except Exception as e:
            print(f"Error computing analysis: {e}")
            raise

    def plot_data(self, word_counts: list, save_path: Optional[str] = None) -> None:
        # Creating a bar chart of word counts
        plt.figure(figsize=(10, 5))
        plt.bar(range(len(word_counts)), word_counts, color='blue')
        plt.xlabel('Article Index')
        plt.ylabel('Word Count')
        plt.title('Word Counts of NYT Articles')

        # Save the plot if a save_path is provided
        if save_path:
            plt.savefig(save_path)
            plt.close()  # Close the figure after saving
        else:
            plt.show()

    def notify_done(self, message: str) -> None:
        print(message)