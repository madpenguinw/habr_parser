import logging

import matplotlib.pyplot as plt
from nltk.probability import FreqDist
from wordcloud import WordCloud

from natasha import (
    Doc,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    NamesExtractor,
    PER,
    Segmenter,
)

import logging_config.app_logger

logger = logging.getLogger(__name__)


class CloudMaker():
    """Create a tag cloud"""

    @staticmethod
    def create_cloud(text, dir=''):
        """Create and save tag cloud as image"""
        logger.info('Creating a tag cloud ...')
        text_raw = " ".join(text)
        wordcloud = WordCloud().generate(text_raw)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(dir + 'tag_cloud.png')
        logger.info('The tag cloud was created and saved')

    @staticmethod
    def extract_names(text):
        """Create a dictionary with names, mentioned in text"""

        logger.info('Creating list with persons names ...')

        segmenter = Segmenter()
        morph_vocab = MorphVocab()
        emb = NewsEmbedding()

        morph_tagger = NewsMorphTagger(emb)
        syntax_parser = NewsSyntaxParser(emb)
        ner_tagger = NewsNERTagger(emb)
        names_extractor = NamesExtractor(morph_vocab)

        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)
        doc.tag_ner(ner_tagger)

        for span in doc.spans:
            span.normalize(morph_vocab)

        for span in doc.spans:
            if span.type == PER:
                span.extract_fact(names_extractor)

        names_list = set()
        for el in doc.spans:
            if el.fact:
                names_list.add(el.normal)

        logger.info('List with persons names is ready')
        return names_list

    @staticmethod
    def most_common_words(text, amount):
        """Return most common words"""
        fdist = FreqDist(text)
        word_and_frequency = fdist.most_common(amount)
        words = []
        for pair in word_and_frequency:
            words.append(pair[0])
        return words
