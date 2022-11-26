import json
import logging
import os

import app_logger

logger = logging.getLogger(__name__)


class Writer():
    """Write data in files"""

    @staticmethod
    def write_dictionary_in_file(dictionary, file='result.json'):
        """Writes a dictionary to the data.json file"""
        if dictionary and type(dictionary) == dict:
            json_dumps = json.dumps(dictionary, indent=4, ensure_ascii=False,)
            with open(file, 'a', encoding='utf-8') as outfile:
                outfile.write(json_dumps)
                outfile.write('\n')
            logger.info('Wrote dictionary in file "%(file)s"', {'file': file})
        else:
            logger.error(
                'Ошибка, ф-ия ждет на вход словарь, получено значение - '
                '"%(dictionary)s", типа "%(var_type)s"',
                {'dictionary': dictionary, 'var_type': type(dictionary)}
            )

    @staticmethod
    def write_txt_in_file(text, file='result.txt'):
        if text and (type(text) in [str, list, set]):
            if type(text) == str:
                with open(file, 'a', encoding='utf-8') as outfile:
                    outfile.write(text)
                    outfile.write('\n')
            else:
                with open(file, 'a', encoding='utf-8') as outfile:
                    for word in text:
                        outfile.write(word)
                        outfile.write('\n')
            logger.info('Wrote text in file "%(file)s"', {'file': file})
        else:
            logger.error(
                'Ошибка, ф-ия ждет на вход строку или список, получено '
                'значение - "%(text)s", типа "%(var_type)s"',
                {'text': text, 'var_type': type(text)}
            )


class Reader():
    """Read from files"""

    @staticmethod
    def read_file(file):
        """Read and return text from file"""
        logger.info('Readig text from file "%(file)s" ...', {'file': file})
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as file:
                text = file.read()
                logger.info('The text has been read')
                return text
        else:
            logger.error(
                'There is no file "%(file)s" in current directory',
                {'file', file}
            )
            return None


class Directory:
    """Handle with directories"""

    @staticmethod
    def check_and_make_dir(dir):
        """Checks if the directory exists and makes it, if it doesn't"""
        if not os.path.isdir(dir):
            os.makedirs(dir)
