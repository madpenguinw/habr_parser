import logging
import os
import string

import pymorphy2
from nltk import download, word_tokenize
from nltk.corpus import stopwords

import app_logger
from tasks.stop_words_list import STOP_WORDS
from tasks.file_manager import Writer, Reader

logger = logging.getLogger(__name__)


class TextCleaner():
    """Clean original text and write it in a new file"""

    @staticmethod
    def text_preprocessing(text):
        """Preliminary text processing"""
        logger.info('Cleaning text ...')
        text = text.lower()
        text = TextCleaner.remove_chars_from_text(
            text, string.punctuation + '«»—“”'
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
        return text_tokens

    @staticmethod
    def remove_stop_words(text_tokens):
        """Removing stop words from text"""
        download('stopwords')
        russian_stopwords = stopwords.words("russian")
        russian_stopwords.extend(STOP_WORDS)
        quantity = len(russian_stopwords)
        text_tokens = \
            [token.strip() for token in text_tokens
             if token not in russian_stopwords]
        logger.info(
            'Deleted %(quantity)s stop words from text',
            {'quantity': quantity})
        return text_tokens

    @staticmethod
    def text_lemmatization(text):
        """Lemmatization of a list of words in Russian"""
        morph = pymorphy2.MorphAnalyzer()
        result = []
        for word in text:
            p = morph.parse(word)[0]
            result.append(p.normal_form)
        return result

    @staticmethod
    def main(file):
        text = Reader.read_file(file)
        if not text:
            return None
        text = TextCleaner.text_preprocessing(text)
        text = TextCleaner.text_tokenization(text)
        lemmatized_text = TextCleaner.text_lemmatization(text)
        clean_text = TextCleaner.remove_stop_words(lemmatized_text)
        logger.info('The text is cleaned and lemmatized')
        return clean_text
