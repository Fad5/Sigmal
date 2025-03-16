from config import EDIT_ECO
from managmant_files_dirs import check_files
import os


def get_data_in_js(loading_path) -> list:
    """
    Функция запускает логику работы проверки фалов
    которые есть на экофизике и в таблице google sheets,
    получает json, заберет только название для дальнейшего создания папок

    Возвращает:
    - list_files - список названия папок которые нужно создать
    """
    list_files = check_files.logic_check(loading_path=loading_path)
    name_sample = []
    for i in list_files:
        name_sample.append(i['Name'])
    return name_sample


def create_dirs(save_path: str, list_names: list) -> None:
    """
    Функция создания папок, на вход принимает список с названиями фалов
    """
    for name in list_names:
        os.makedirs(save_path + '/' + str(name), exist_ok=True)


def logic_dir(save_path, loading_path) -> None:
    """
    Логика работы функции
    """
    list_name_dir = get_data_in_js(loading_path)
    # Получает список, переводит в set, для того чтобы получить уникальные значения
    # И обратно переводит в list для дальнейше работы
    create_dirs(save_path, list(set(list_name_dir)))


def get_all_files_if_exist(save_path, loading_path) -> list:
    """
    Получение уже существующих фалов
    Аргументы:
    - save_path - путь где будут храниться файлы

    Возвращает:
    - is_files - список существующих файлов
    """
    dirs = list(set(get_data_in_js(loading_path)))
    print(dirs)
    is_files = []
    for dir_save in dirs:
        try:
            files = os.listdir(save_path+ '/' + dir_save)
            if files:
                for file in files:
                    is_files.append(file[:-4])
        except FileNotFoundError:
            pass
    return is_files