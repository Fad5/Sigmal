import keyboard
import pyautogui
import time
import platform
import os
import pyperclip
import re

from config import path_btn_pputest, path_btn_signal


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
    for i in path_btn_pputest, path_btn_signal:
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
