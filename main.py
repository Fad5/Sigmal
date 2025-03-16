import time
from tkinter import filedialog

from Google_sheets import process_csv, create_csv_file
from config import LINK_TIME_SAMPLE, SAMPLE
from managmant_files_dirs.Create_dir import logic_dir
from managmant_files_dirs.Hadler_file import JsonHandler
from signal_ import management_signal


def path_save() -> tuple:
    """
    Открывает два диалоговых окна для выбора директорий.

    Первое окно позволяет выбрать папку, в которой находятся файлы экофизики.
    Второе окно позволяет выбрать папку для сохранения файлов.

    Возвращает:
        tuple: Кортеж из двух строк, каждая из которых содержит путь к выбранной папке.
               Filepath — путь к папке с файлами экофизики,
               save_path — путь к папке для сохранения.
    """
    loading_path = filedialog.askdirectory(title="Выберите папку в которой находятся файлы экофизики")
    save_path = filedialog.askdirectory(title="Выберите папку сохранения")
    return loading_path, save_path


def download_files() -> None:
    """
    Функция для скачивания csv файлов и преобразования из в json файлы
    """
    create_csv_file(f'{SAMPLE}/export?format=csv', 'sample_sizes')
    sample_sizes = process_csv('sample_sizes', mode='default')
    JsonHandler.write_json('sample_sizes', sample_sizes)
    time.sleep(2)

    create_csv_file(f'{LINK_TIME_SAMPLE}/export?format=csv', 'sample_time')
    sample_time = process_csv('sample_time', 'signal')
    JsonHandler.write_json('sample_time', sample_time)


def main() -> None:
    # loading_path, save_path = path_save()
    loading_path = 'C:/Users/Fad/Desktop/Работа/1'
    save_path = 'F:/Протоколы'
    download_files()
    logic_dir(save_path=save_path, loading_path=loading_path)
    management_signal(save_path, loading_path)
    print("В С Ё !!!")


"""
Логика программы 

1. Запускается программа, у пользователя спрашивает из какой папки брать файлы экофизики, 
и как сохранять данные после обработке

2.Переменные находятся в файле майне и запускается функцией main()

3. Сохраняется в файле под название setting.json
"""

if __name__ == "__main__":
    main()
