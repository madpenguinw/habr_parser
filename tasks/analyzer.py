import logging

import matplotlib.pyplot as plt
from wordcloud import WordCloud

import app_logger

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
