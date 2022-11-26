import logging

import logging_config.app_logger
from tasks.analyzer import CloudMaker
from tasks.cleaner import TextCleaner
from tasks.parser import Parser
from tasks.writer import Writer

logger = logging.getLogger(__name__)


def main():
    """
    Receives and processes a request to
    parse the Habr.com website and other tasks
    """
    task = int()
    while task != 4:
        try:
            task = int(input(
                'Введите номер задания, которое вас интересует '
                '(1, 2, 3 или 4) \n'
                '1 - Поиск статей по ключевым словам на Habr.com \n'
                '2 - Получение текста определенной статьи на Habr.com '
                '(например, для дальнейшего построения облака тегов) \n'
                '3 - Построение облака тегов \n'
                '4 - Выход из программы \n'
            ))
        except TypeError:
            logger.error('A digit must be entered \n')
        if task not in range(1, 5):
            while task not in range(1, 5):
                try:
                    task = int(input(
                        'Вы ввели недопустимое значение. '
                        'Ведите цифру: 1, 2, 3 или 4 \n'))
                except ValueError:
                    logger.error('A digit must be entered \n')
        if task == 1:
            slug = input(
                'Введите ключевое слово или слова для поиска на '
                'Habr.com \n')
            certain_page = -1
            while certain_page not in range(51):
                try:
                    certain_page = int(input(
                        'Введите номер страницы, информацию с которой '
                        'хотите получить (от 1 до 50) \n'
                        'Или введите 0, чтобы получить информацию '
                        'со всех страниц \n'))
                except ValueError:
                    logger.error('Number must be entered in digits')
            Parser.parsing_and_saving_results(slug, certain_page)
        elif task == 2:
            condition = False
            while not condition:
                url = input('Введите url статьи на Habr.com или ее id \n')
                try:
                    is_article_id = int(url)
                    url = Parser.make_habr_url(is_article_id)
                    condition = True
                except ValueError:
                    checking_url = Parser.check_is_habr_url(url)
                    if checking_url:
                        condition = True
                    else:
                        logger.error('Please enter a valid value')
            text = Parser.get_text_from_aricle(url)
            Writer.write_txt_in_file(text)

        elif task == 3:
            text = TextCleaner.main()
            if text:
                top_ten = CloudMaker.most_common_words(text, 10)
                CloudMaker.create_cloud(top_ten)

        elif task == 4:
            print('Выполняется выход из программы ... \n'
                  'Хорошего дня!')


if __name__ == '__main__':
    main()
