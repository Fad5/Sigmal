import os

import pyautogui

from managmant_files_dirs.Create_dir import get_all_files_if_exist
from managmant_files_dirs.check_files import logic_check, get_files_edit
from menegmant_keyboard.menegment_keyboard import search_eco, save_file_csv
from utils import wait_loading, correct_name_file_csv
from config import path_btn_signal


def first_point():
    """
    Получает список координат всех инпутов и возвращает 

    Аргументы:
    - list_screens - список скриншотов инпутов в формате PNG
    """
    list_screens =  os.listdir('btn/btn_signal/')
    print(list_screens)
    list_points = []
    for screen in list_screens:  # Проходимся по списку циклом
        if screen[1:] in ['.png', '.PNG']:
            # Добавляем к названию файла папку, аргумент
            # confidence показывает с какой точностью искать
            location = pyautogui.locateOnScreen('btn/btn_signal/' + screen, confidence=0.78)
            list_points.append({screen[:-4]: location})
            pyautogui.click(location)
        else:
            pass
    return list_points


def management_signal(save_path, loading_path) -> None:
    """
    Основная функция обработки данных.
    
    Описание:
    1. Получает список образцов с помощью `logic_check()`.
    2. Получает список существующих файлов через `get_all_files_if_exist()`.
    3. Для каждого образца:
        - Генерирует имя файла через `correct_name_file_csv()`.
        - Проверяет, существует ли файл.
            Если да — выводит сообщение и переходит к следующему образцу.
        - Выполняет поиск `search_eco()` по времени образца.
        - Сохраняет данные в CSV-файл с помощью `save_file_csv()`.
        - Ожидает завершения сохранения через `wait_loading()`.
        - Выводит сообщение о завершении обработки.
    """
    exist_files = set(get_all_files_if_exist(save_path=save_path,loading_path=loading_path))
    
    for sample in logic_check(loading_path):
        name_file = correct_name_file_csv(sample['Name'], sample['Press'])
        if name_file in exist_files:
            print(f"{sample['Name']} уже существует")
            continue

        first_point()
        search_eco(sample['Time'], loading_path=loading_path)
        save_file_csv(sample['Name'], sample['Press'],save_path=save_path)
        wait_loading('btn/btn_signal/save/2.png')
        print(f"{sample['Name']} готово")

