# analysis.py

from typing import Any, Optional
import yaml
import requests
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class Analysis:

    def __init__(self, analysis_config: str) -> None:
        self.CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']
        self.config = {}
        self.dataset = None
        self.load_data()

    def load_data(self) -> None:
        try:
            for path in self.CONFIG_PATHS + [analysis_config]:
                with open(path, 'r') as f:
                    this_config = yaml.safe_load(f)
                self.config.update(this_config)

            # Loading NYT API key from YAML file
            with open(self.config['secrets_file']) as f:
                nyt_secrets = yaml.safe_load(f)

            # Retrieving data from NYT API
            api_key = nyt_secrets['API_key']
            nyt_url = 'https://api.nytimes.com/svc/archive/v1/2019/1.json'
            params = {'api-key': api_key}
            self.dataset = requests.get(nyt_url, params=params).json()

        except Exception as e:
            logger.error(f"Error loading data: {e}")
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
            logger.error(f"Error computing analysis: {e}")
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

# Unit Test for `compute_analysis` method
def test_compute_analysis():
    analysis_instance = Analysis(analysis_config='path/to/analysis_config.yml')
    result = analysis_instance.compute_analysis()
    assert isinstance(result, float)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Example usage
if __name__ == "__main__":
    analysis_instance = Analysis(analysis_config='path/to/analysis_config.yml')
    result = analysis_instance.compute_analysis()
    analysis_instance.notify_done(f"Analysis complete. Average Word Count: {result}")
