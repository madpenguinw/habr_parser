import logging

import logging_config.app_logger
from tasks.analyzer import CloudMaker
from tasks.cleaner import TextCleaner
from tasks.file_manager import Directory, Reader, Writer
from tasks.parser import Parser

logger = logging.getLogger(__name__)


def main():
    """
    Receives and processes a request to
    parse the Habr.com website and other tasks
    """
    task = int()
    while task != 5:
        try:
            task = int(input(
                'Введите номер задания, которое вас интересует '
                '(1, 2, 3, 4 или 5) \n'
                'Все полученные результаты будут сохранены в папку results \n'
                '1 - Поиск статей по ключевым словам на Habr.com \n'
                '2 - Получение текста определенной статьи на Habr.com \n'
                '3 - Построение облака тегов из текста статьи \n'
                '4 - Формирование списка людей, упомянутых в тексте статьи \n'
                '5 - Выход из программы \n'
            ))
            Directory.check_and_make_dir('results')
        except ValueError:
            logger.error('A digit must be entered \n')
        if task not in range(1, 6):
            while task not in range(1, 6):
                try:
                    task = int(input(
                        'Вы ввели недопустимое значение. '
                        'Ведите цифру: 1, 2, 3, 4 или 5 \n'))
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
            parsing_results = Parser.main(slug, certain_page)
            Writer.write_dictionary_in_file(
                parsing_results, 'results/data.json')

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
            Writer.write_txt_in_file(text, file='results/text.txt')

        elif task == 3:
            text = Reader.read_file('results/text.txt')
            if text:
                clean_text = TextCleaner.main(text)
                Writer.write_txt_in_file(
                    clean_text, file='results/clean_text.txt')
                top_ten = CloudMaker.most_common_words(clean_text, 10)
                CloudMaker.create_cloud(top_ten, 'results/')

        elif task == 4:
            text = Reader.read_file('results/text.txt')
            if text:
                names_list = CloudMaker.extract_names(text)
                Writer.write_txt_in_file(
                    names_list, file='results/persons.txt')

        elif task == 5:
            print('Выполняется выход из программы ... \n'
                  'Хорошего дня!')


if __name__ == '__main__':
    main()
