import os
from managmant_files_dirs.Hadler_file import JsonHandler
from config import EDIT_ECO, name_file_sample


def get_files_edit(path_files: str) -> list:
    """
    Получаем файлы с ЭКОФИЗИКИ

    Аргументы:
    - path_files - Путь к файлам EDT

    Возвращает:
    - files - файлы с ЭКОФИЗИКИ
    """
    files = os.listdir(path_files)
    return files


def correct_name_files(list_files_edt: list) -> list:
    """
    Проверяем чтобы формат файлы были формата EDT, переводим в str и возвращаем

    Аргументы:
    - name_files - файлы с ЭКОФИЗИКИ

    Возвращает:
    - list_correct_edt - список файлов которые прошли проверку
    """
    list_correct_edt = []
    for file in list_files_edt:
        if file[9:] == 'EDT':
            list_correct_edt.append(str(file[:5]).replace('_', '-'))
    return list_correct_edt


def check(list_name_files: list, json_data: dict) -> list:
    """
    Проверяем чтобы в папке файлы и из google sheet сходились

    Аргументы:
    - list_name_files - список образцов
    - json_data - файл json с данными из размерного файла с образцами после испытания

    Возвращает:
    - exits_file_in_table - список файлов которые сходятся с разменным файлом
    """

    exits_file_in_table = []
    not_exits_files = []
    for i in json_data:
        if i['Time'] in list_name_files:
            exits_file_in_table.append(i)
        else:
            not_exits_files.append(i['Name'])
    print('Нет таких файлов' + str(not_exits_files))
    return exits_file_in_table


def logic_check(loading_path:str) -> list:
    """
    Прописана логика файла

    Возвращает:
    - loading_path - путь к файлам экофизики
    """
    samples_press = JsonHandler.read_json(name_file_sample)  # Получаем данные с json файла
    files = get_files_edit(loading_path)  # Получаем файлы
    correct_files = correct_name_files(files)  # Проверяем файлы
    list_files = check(correct_files, samples_press)  # Сверяем файлы экофизики с google sheet
    return list_files
