import logging
import os
import string

from nltk import Text, download, word_tokenize  # TODO
from nltk.corpus import stopwords

import app_logger

logger = logging.getLogger(__name__)


class TextCleaner():
    """Clean original text and write it in a new file"""

    @staticmethod
    def write_clean_text(clean_text):
        """Write clean text in file"""
        with open('clean_text.txt', 'a', encoding='utf-8') as file:
            for word in clean_text:
                file.write(word)
                file.write('\n')
        logger.info('File with the cleaned text is ready')

    @staticmethod
    def get_text_from_file():
        """Read and return text from file 'text.txt'"""
        if os.path.isfile('text.txt'):
            logger.info('Readig text from file ...')
            file = open('text.txt', "r", encoding="utf-8")
            text = file.read()
            return text
        else:
            logger.error('There is no file text.txt in current directory')
            return None

    @staticmethod
    def text_preprocessing(text):
        """Preliminary text processing"""
        logger.info('Cleaning text ...')
        text = text.lower()
        text = TextCleaner.remove_chars_from_text(
            text, string.punctuation + '«»—'
        )
        text = TextCleaner.remove_chars_from_text(text, string.digits)
        return text

    @staticmethod
    def remove_chars_from_text(text, chars):
        """Removing waste chars from text"""
        full_text = str()
        for ch in text:
            if ch in chars:
                full_text += ' '
            else:
                full_text += ch
        return full_text

    @staticmethod
    def text_tokenization(text):
        """Splits the cleaned text into its component parts - tokens"""
        download('punkt')
        text_tokens = word_tokenize(text)
        # text = Text(text_tokens)
        return text_tokens

    @staticmethod
    def remove_stop_words(text_tokens):
        """Removing stop words from text"""
        download('stopwords')
        russian_stopwords = stopwords.words("russian")
        russian_stopwords.extend(['это'])
        quantity = len(russian_stopwords)
        text_tokens = \
            [token.strip() for token in text_tokens
             if token not in russian_stopwords]
        logger.info(
            'Deleted %(quantity)s stop words from text',
            {'quantity': quantity})
        return text_tokens

    @staticmethod
    def main():
        text = TextCleaner.get_text_from_file()
        if not text:
            return None
        text = TextCleaner.text_preprocessing(text)
        text = TextCleaner.text_tokenization(text)
        clean_text = TextCleaner.remove_stop_words(text)
        logger.info('The text is cleaned')
        TextCleaner.write_clean_text(clean_text)
        return clean_text