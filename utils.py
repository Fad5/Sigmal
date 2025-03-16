import pprint

import keyboard
import pyautogui
import time
import platform
import os
import pyperclip
import re

from config import path_btn_signal
from managmant_files_dirs.Hadler_file import JsonHandler


def correct_name_file_csv(name: str, press: str) -> str:
    """
    Функция для создания имени файла в который
    входит названия образца и пригруз

    Аргументы:

    - name - названия образца
    - press - масса пригруза
    """
    new_name = str(name) + f'({str(press)})'
    return str(new_name)


def wait_loading(screen_path: str) -> None:
    """
    Функция для ожидания загрузки программы signal

    Принцип работы:
    Работает по принципу когда будет соответствие с этим скриншотом
    программа продолжит свою работу когда найдет это изображение

    Аргументы:
    - screen_path - скриншот
    """
    time.sleep(1)
    i = 0
    while i < 1:
        time.sleep(0.5)
        print('Waiting')
        try:
            location = pyautogui.locateOnScreen(screen_path, confidence=0.80)
            print(location)
            i += 1
        except:
            i = 0


def check_platform() -> tuple:
    """
    Функция для отслеживания версии windows

    Возвращает:
    - version_platform - список с данными о платформе
    """
    version_platform = platform.win32_ver()
    return version_platform


def paste(text: str):
    """
    Функция имитации нажатия ctrl + v
    и вставки текста

    Аргументы:
    - text - текст который нужно вставить
    """
    pyperclip.copy(text)  # Копируем новый текст в буфер обмена
    keyboard.press_and_release('ctrl + v')  # Эмулируем нажатие Ctrl + V (вставку)


def timeout_step() -> None:
    """
    Функция паузы
    """
    time.sleep(1.3)


def create_dir() -> None:
    """
    Функция для создания корневых папок в которых будут храниться скриншоты кнопок
    """
    for i in path_btn_signal:
        os.makedirs(i, exist_ok=True)


def search_eco(name_file: str, loading_path) -> None:
    """
    Функция для поиска файлов
    """
    timeout_step()
    keyboard.add_hotkey("ctrl+l", lambda: print("ctrl+alt+j was pressed"))
    pyautogui.hotkey('ctrl', 'l')
    timeout_step()
    paste(loading_path)
    timeout_step()
    pyautogui.press('enter')
    timeout_step()
    pyautogui.hotkey('ctrl', 'f')
    timeout_step()
    paste(name_file)
    timeout_step()

    for _ in range(2): pyautogui.press('down')
    timeout_step()
    for _ in range(4): pyautogui.press('up')
    btn_open = pyautogui.locateOnScreen('btn/btn_signal/save/open.png', confidence=0.82)
    if btn_open:
        pyautogui.click(btn_open)
    else:
        print("Кнопка 'Открыть' не найдена.")


def fill_fields(coordinates, loading_path, data_upload):
    global cargo_, under_load
    count = 0
    list_file = get_files_and_sort(loading_path)
    for field, (x, y) in coordinates.items():
        data_file = list_file[count]
        name, cargo = get_name_upload(data_file)
        for i in data_upload:
            if i['Name'] == name and i['Press'] == cargo:
                cargo_ = i['Press']
                under_load = i['Under_load']

        if count == 0:
            pyautogui.click(x, y)
            search_eco(loading_path=loading_path, name_file=data_file)
            count += 1

        if count == 1:
            pyautogui.click(x, y)
            paste(cargo_)
        else:
            time.sleep(1)
            pyautogui.click(x, y)
            paste(under_load)
            print(f"Заполнено {field} по координатам ({x}, {y})")


# Функция для извлечения числа из строки
def extract_number(filename):
    match = re.search(r'\((\d+)\)', filename)  # Ищем число в скобках
    return int(match.group(1)) if match else 0  # Преобразуем в int


def get_files_and_sort(path):
    files = os.listdir(path)
    sorted_files = sorted(files, key=extract_number)
    return sorted_files


def get_name_upload(filename):
    start = filename.find('(')
    end = filename.find(')')
    cargo = (filename[start + 1:end])
    name = (filename[:start])
    return name, cargo


def get_full_data():
    """
    Читает данные из JSON-файлов sample_sizes.json и sample_time.json.

    :return: Кортеж из двух списков samples_press и samples_time
    """
    samples_press = JsonHandler.read_json('sample_sizes.json')
    samples_time = JsonHandler.read_json('sample_time.json')
    return samples_press, samples_time

def unique_names_samples(samples_time):
    """
    Извлекает уникальные названия образцов из списка samples_time.

    :param samples_time: Список словарей с ключом 'Name'
    :return: Список уникальных названий образцов
    """
    list_names = [i['Name'] for i in samples_time]
    return list(set(list_names))

def group_by_name(samples_time, list_names_unique):
    """
    Группирует данные по названиям образцов.

    :param samples_time: Список данных о времени испытаний
    :param list_names_unique: Список уникальных названий образцов
    :return: Список словарей с объединенными данными по каждому уникальному образцу
    """
    full_data_load = []
    for name in list_names_unique:
        list_group_data = [
            {"Press": item['Press'], "Under_load": item['Under_load']}
            for item in samples_time if item['Name'] == name
        ]
        full_data_load.append({'Name': name, 'Width': list_group_data})
    return full_data_load

def map_press_to_load(samples_press, full_data_load):
    """
    Объединяет данные samples_press с full_data_load по полю 'Name'.

    :param samples_press: Список характеристик образцов (размеры, вес)
    :param full_data_load: Список данных по нагрузке для каждого образца
    :return: Список словарей, содержащих полные данные об образцах
    """
    list_data = [
        {
            "Height": press['Height'],
            "Length": press['Length'],
            "Name": press['Name'],
            "Weight": press['Weight'],
            "Width": press['Width'],
            "Under_load": load['Width']
        }
        for press in samples_press
        for load in full_data_load
        if press['Name'] == load['Name']
    ]
    return list_data

def get_full_sample_data():
    """
    Собирает полные данные об образцах, объединяя информацию о размерах, весе и нагрузке.

    :return: Список словарей с полной информацией об образцах
    """
    samples_press, samples_time = get_full_data()
    list_names_unique = unique_names_samples(samples_time)
    full_data_load = group_by_name(samples_time, list_names_unique)
    result = map_press_to_load(samples_press, full_data_load)
    JsonHandler.write_json('data', result)









