import pandas as pd
import csv
from managmant_files_dirs.Hadler_file import JsonHandler


def create_csv_file(url: str, name_save_file: str) -> None:
    """
    Загружает онлайн-таблицу Google, обрабатывает её с помощью pandas и сохраняет в CSV-файл.
    """
    df = pd.read_csv(url)

    # Выбираем только нужные столбцы
    selected_columns = df.columns[:18]  # Берем первые 18 столбцов
    new_df = df[selected_columns]

    # Экспортируем в CSV
    new_df.to_csv(f'{name_save_file}.csv', index=False)
    print("CSV-файл успешно создан.")


def process_csv(name_file: str, mode='default'):
    """
    Читает CSV-файл и преобразует данные в JSON-формат.
    
    Параметры:
    - name_file (str): Имя файла без расширения.
    - mode (str): Режим обработки ('default' или 'signal').
    
    Возвращает:
    - data (list): Данные в формате JSON.
    """
    # Чтение CSV-файла
    with open(f'{name_file}.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Фильтрация строк и формирование списка словарей
        filtered_data = []
        if mode == 'default':
            for row in reader:
                if 'СТ-' in row[0]:
                    if row[2] and row[3] and row[4]:
                        filtered_data.append({
                            'Name': row[0],
                            'Width': row[5],
                            'Length': row[10],
                            'Height': row[15],
                            'Weight': row[16],
                            'Press': row[17]
                        })
        if mode == 'signal':
            for row in reader:
                if row[0] and row[1] and row[2]:
                    filtered_data.append({
                        'Time': row[0],
                        'Name': row[1],
                        'Press': row[2],
                        'Under_load': row[3]
                    })

    return filtered_data
