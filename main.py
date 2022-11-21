import logging

from parser import Parser

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


def main():
    """Receives and processes a request to parse the Habr.com website"""
    answer = str()
    task = int()
    while answer != 'no':
        try:
            task = int(input(
                'Введите номер задания, которое вас интересует '
                '(1, 2 или 3) \n'
                '1 - Поиск статей по ключевым словам на Habr.com \n'
                '2 - Получение текста определенной статьи на Habr.com '
                '(например, для дальнейшего построения облака тегов) \n'
                '3 - Построение облака тегов \n'
            ))
        except TypeError:
            print('Ошибка: число необходимо необходимо вводить цифрами \n')
        if task not in range(1, 4):
            while task not in range(1, 4):
                try:
                    task = int(input(
                        'Вы ввели недопустимое значение. '
                        'Ведите цифру 1 или 2  \n'))
                except ValueError:
                    print('Ошибка: число необходимо необходимо вводить '
                          'цифрами \n')
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
                except ValueError:  # TODO это надо проверить
                    print('Ошибка: число необходимо необходимо вводить '
                          'цифрами')
            Parser.parsing_and_saving_results(slug, certain_page)
            answers = ['yes', 'no']
            answer = input('Хотите продолжить? (yes/no) \n')
            while answer not in answers:
                answer = input(
                    'Введите без кавычек "yes", если хотите продолжить'
                    'работу с парсером или "no", если хотите закончить \n')
        elif task == 2:
            pass

        elif task == 3:
            pass


if __name__ == '__main__':
    main()
