import logging

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.probability import FreqDist

import logging_config.app_logger

logger = logging.getLogger(__name__)


class CloudMaker():
    """Create a tag cloud"""

    @staticmethod
    def create_cloud(text):
        logger.info('Creating a tag cloud ...')
        text_raw = " ".join(text)
        wordcloud = WordCloud().generate(text_raw)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig('tag_cloud.png')
        logger.info('The tag cloud was created and saved')

    @staticmethod
    def most_common_words(text, amount):
        """Return most common words"""
        fdist = FreqDist(text)
        word_and_frequency = fdist.most_common(amount)
        words = []
        for pair in word_and_frequency:
            words.append(pair[0])
        return words
