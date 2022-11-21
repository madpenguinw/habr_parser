import json
import logging
from datetime import datetime
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

from bs4 import BeautifulSoup

FORMAT = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
DATEFMT = '%Y-%m-%dT%H:%M:%S'

logging.basicConfig(
    format=FORMAT,
    datefmt=DATEFMT,
    level=logging.INFO,
)

formatter = logging.Formatter(
    FORMAT,
    datefmt=DATEFMT
)


logger = logging.getLogger(__name__)


class CustomError(Exception):
    pass


class Parser():
    """Parsing site Habr.com"""

    @staticmethod
    def json_preparing():
        """Prepares empty dictionaries"""
        author_dict = {
            'id': False,
            'nickname': False,
            'name': False,
            'speciality': False,
            'link': False,
        }
        article = {
            'time_published': False,
            'title': False,
            'author': {},
            'link': False,
        }
        data = {}
        json_response = {
            'actual_data': False,
            'current_processing_duration': False,
            'error_message': False,
            'is_error': False,
            'origin_request': False,
            'response_status': False,
            'status_code': False,
            'data': {},
        }
        return author_dict, article, data, json_response

    @staticmethod
    def current_time():
        """Returns the time and date in the correct format"""
        date_time = str(datetime.now())
        date, time = date_time.split(' ')
        time = time[:8]
        formated = date + 'T' + time
        return formated

    @staticmethod
    def make_slug(slug):
        """Adds spaces to the slug"""
        if ' ' in slug:
            slug_list = slug.split(' ')
            itteriation = 1
            slug = ''
            for word in slug_list:
                if itteriation != 1:
                    slug += '%20'
                word = quote(word)
                slug += word
        return slug

    @staticmethod
    def get_all_arcticles_ids(slug, certain_page=None):
        """
        Returns a list containing lists with id of all articles from all pages,
        found by keywords on Habr.com, or from one certain
        page, when certain_page param is set
        """
        logger.info('Getting articles ids')
        all_ids_list = []
        # There might be max 50 pages with results on Habr.com
        for page in range(1, 51):
            if certain_page:
                page = certain_page
            url = \
                f'https://habr.com/ru/search/page{page}/?q=' \
                f'{quote(slug)}&target_type=posts&order=relevance'
            try:
                html = urlopen(url).read()
            except HTTPError:
                return all_ids_list
            bs = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
            content = bs.find_all('script')[4]
            if str(content).startswith('<script async=""'):
                content = bs.find_all('script')[5]
            my_text = content.text.split('=', maxsplit=1)[1]
            my_text = my_text[: -4]
            my_text = str(my_text)
            if f'"articlesIds":"SEARCH_QUERY_RESULTS_PAGES_{page}":[]' \
                    in my_text:
                raise CustomError(f'По запросу "{slug}" ничего не найдено')
            articles_ids = my_text.split(
                f'"SEARCH_QUERY_RESULTS_PAGES_{page}":["', maxsplit=1)[1]
            articles_ids = articles_ids.split('"]}', maxsplit=1)[0]
            list_articles_ids = articles_ids.split('","')
            all_ids_list.append(list_articles_ids)
            if certain_page:
                break
        return all_ids_list

    @staticmethod
    def get_author_dict(bs_str):
        """
        Returns a dictionary with information about
        the author of the article
        """
        try:
            author_dict = Parser.json_preparing()[0]
            author_info = bs_str.split('"author":{"id":"', maxsplit=1)[1]
            author_info = author_info.split('}', maxsplit=1)[0]
            author_id = author_info
            author_id = author_info.split('","', maxsplit=1)[0]
            author_nickname = author_info
            author_nickname = author_nickname.split(
                '"alias":"', maxsplit=1)[1]
            author_nickname = author_nickname.split('","', maxsplit=1)[0]
            author_name = author_info
            author_name = author_name.split('"fullname":', maxsplit=1)[1]
            author_name = author_name.split(',"', maxsplit=1)[0]
            if '"' in author_name:
                author_name = author_name.replace('"', '')
            author_dict['id'] = author_id
            author_dict['nickname'] = author_nickname
            author_dict['name'] = author_name
            author_dict['link'] = \
                f'https://habr.com/ru/users/{author_nickname}/posts/'
            if '"speciality":"' in author_info:
                author_speciality = author_info
                author_speciality = author_speciality.split(
                    '"speciality":"', maxsplit=1)[1]
                author_speciality = author_speciality.split(
                    '\","', maxsplit=1)[0]
                author_dict['speciality'] = author_speciality
        except Exception as error:
            error = str(error)
            logger.error(error)
        return author_dict

    @staticmethod
    def get_one_arcticle_info(article_id):
        """Returns a dictionary with full information about the article"""
        article_url = f'https://habr.com/ru/post/{article_id}/'
        html = urlopen(article_url).read()
        bs = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
        bs_str = str(bs)
        article_dict = Parser.json_preparing()[1]
        title = bs.find('title').text
        article_dict['title'] = title
        article_dict['link'] = article_url
        try:
            time_published = bs_str.split(
                '"timePublished":"', maxsplit=1)[1]
        except IndexError:
            time_published = time_published.split(
                '"timePublished":"', maxsplit=1)[0]
        # Removed +00:00 from the time_published
        # so the format matches actual_data
        time_published = time_published.split('+', maxsplit=1)[0]
        article_dict['time_published'] = time_published
        author_dict = Parser.get_author_dict(bs_str)
        article_dict['author'] = author_dict
        return article_dict

    @staticmethod
    def main_parser(slug, certain_page):
        """The main function for parsing"""
        start_time = datetime.now()
        logger.info('Began processing request "%(slug)s"', {'slug': slug})
        data, json_response = Parser.json_preparing()[2: 4]
        json_response['actual_data'] = Parser.current_time()
        json_response['origin_request'] = slug
        slug = Parser.make_slug(slug)
        try:
            all_arcticles_ids = Parser.get_all_arcticles_ids(
                slug, certain_page)
            logger.info('Got all articles ids')
            i = 1
            for list_articles_ids in all_arcticles_ids:
                for article_id in list_articles_ids:
                    logger.info('Processing article number  %(i)s, id = %(article_id)s', {'i': i, 'article_id': article_id})
                    article_dict = Parser.get_one_arcticle_info(article_id)
                    # data{} contains data about all articles
                    data[i] = article_dict
                    i += 1
            logger.info('Got info about all articles')
            # json_response{} contains all data for the request
            json_response['data'] = data
            processing_time = datetime.now() - start_time
            processing_time = processing_time.total_seconds()
            json_response['current_processing_duration'] = processing_time
            json_response['response_status'] = 'COMPLETE'
            json_response['status_code'] = 200
            return json_response
        except Exception as error:
            error = str(error)
            json_response['error_message'] = error
            json_response['is_error'] = True
            processing_time = datetime.now() - start_time
            processing_time = processing_time.total_seconds()
            json_response['current_processing_duration'] = processing_time
            json_response['response_status'] = 'FAILED'
            json_response['status_code'] = 404
            logger.info("Parser's job is done here")
            return json_response

    @staticmethod
    def write_json_in_file(dictionary):
        """Writes a dictionary to the data.json file"""
        json_dumps = json.dumps(dictionary, indent=4, ensure_ascii=False,)
        with open('data.json', 'a', encoding='utf-8') as outfile:
            outfile.write(json_dumps)
            outfile.write('\n')

    @staticmethod
    def parsing_and_saving_results(slug, certain_page):
        """Running the parser and saving the result to a file"""
        response = Parser.main_parser(slug, certain_page)
        Parser.write_json_in_file(response)
