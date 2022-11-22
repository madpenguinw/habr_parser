import json
import logging


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


class Writer():
    """Write data in files"""

    @staticmethod
    def write_dictionary_in_file(dictionary):
        """Writes a dictionary to the data.json file"""
        if dictionary and type(dictionary) == dict:
            json_dumps = json.dumps(dictionary, indent=4, ensure_ascii=False,)
            with open('data.json', 'a', encoding='utf-8') as outfile:
                outfile.write(json_dumps)
                outfile.write('\n')
            logger.info('Wrote dictionary in file')
        else:
            logger.error(
                'Ошибка, ф-ия ждет на вход словарь, получено значение - '
                '"%(dictionary)s", типа "%(var_type)s"',
                {'dictionary': dictionary, 'var_type': type(dictionary)}
            )

    @staticmethod
    def write_txt_in_file(text):
        if text and type(text) == str:
            with open('text.txt', 'a', encoding='utf-8') as outfile:
                outfile.write(text)
                outfile.write('\n')
            logger.info('Wrote text in file')
        else:
            logger.error(
                'Ошибка, ф-ия ждет на вход текст (строку), получено '
                'значение - "%(text)s", типа "%(var_type)s"',
                {'text': text, 'var_type': type(text)}
            )


if __name__ == '__main__':
    Writer.write_txt_in_file(1)
        