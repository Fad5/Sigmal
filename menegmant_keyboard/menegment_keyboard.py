import keyboard
import pyautogui

from config import SAVE_DIR, EDIT_ECO
from utils import timeout_step, correct_name_file_csv, paste


def search_eco(time_file: str, loading_path) -> None:
    """
    Функция для поиска файлов
    """
    timeout_step()
    keyboard.add_hotkey("ctrl+l", lambda: print("ctrl+alt+j was pressed"))
    pyautogui.hotkey('ctrl', 'l')
    timeout_step()
    # pyautogui.write(loading_path)
    paste(loading_path)
    timeout_step()
    pyautogui.press('enter')
    timeout_step()
    pyautogui.hotkey('ctrl', 'f')
    timeout_step()
    pyautogui.write(time_file.replace('-', '_'))
    timeout_step()

    for _ in range(2): pyautogui.press('down')
    timeout_step()
    for _ in range(4): pyautogui.press('up')
    btn_open = pyautogui.locateOnScreen('btn/btn_signal/save/open.png', confidence=0.82)
    if btn_open:
        pyautogui.click(btn_open)
    else:
        print("Кнопка 'Открыть' не найдена.")


def save_file_csv(name, press, save_path):
    timeout_step()
    pyautogui.press('delete')
    paste(str(correct_name_file_csv(name, press)))
    timeout_step()
    pyautogui.hotkey('ctrl', 'l')
    paste(f"{save_path}/{name}")
    pyautogui.press('enter')
    if btn := pyautogui.locateOnScreen('btn/btn_signal/save/save.png', confidence=0.80): pyautogui.click(btn)
