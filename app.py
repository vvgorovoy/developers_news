import PySimpleGUI as sg
import os
from datetime import datetime

# Списки застройщиков и категорий новостей
developers = ['ПИК', 'ЛСР', 'ФСК', 'Донстрой']
news_categories = ['Категория 1', 'Категория 2', 'Категория 3']

sg.theme('LightBrown1')

# Функция для создания окна
def create_window():
    layout = [
        [sg.Text('Выберите застройщиков')],
        [sg.Listbox(developers, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(30, 6), key='-DEVELOPERS-')],
        [sg.Button('Добавить застройщика'), sg.Button('Удалить застройщика')],
        
        [sg.Text('Выберите категории новостей')],
        [sg.Listbox(news_categories, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(30, 6), key='-CATEGORIES-')],
        [sg.Button('Добавить категорию'), sg.Button('Удалить категорию')],
        
        [sg.Text('Дата начала:'), sg.Input(key='-START_DATE-', size=(10, 1)), sg.CalendarButton('Выбрать', target='-START_DATE-', format='%Y-%m-%d')],
        [sg.Text('Дата окончания:'), sg.Input(key='-END_DATE-', size=(10, 1)), sg.CalendarButton('Выбрать', target='-END_DATE-', format='%Y-%m-%d')],
        
        [sg.Text('Выберите путь к выходному файлу (.xls):'), sg.Input(key='-FILE_PATH-', size=(25, 1)), sg.FileSaveAs('Обзор', file_types=(('Excel Files', '*.xls'),))],
        
        [sg.Button('Сформировать выгрузку'), sg.Button('Выход')]
    ]
    
    return sg.Window('Парсинг новостей', layout)

# Основной цикл
window = create_window()
while True:
    event, values = window.read()
    
    if event in (sg.WINDOW_CLOSED, 'Выход'):
        break
    
    elif event == 'Добавить застройщика':
        new_developer = sg.popup_get_text('Введите имя застройщика:')
        if new_developer:
            developers.append(new_developer)
            window['-DEVELOPERS-'].update(developers)
    
    elif event == 'Удалить застройщика':
        selected = values['-DEVELOPERS-']
        for item in selected:
            developers.remove(item)
        window['-DEVELOPERS-'].update(developers)
    
    elif event == 'Добавить категорию':
        new_category = sg.popup_get_text('Введите название категории:')
        if new_category:
            news_categories.append(new_category)
            window['-CATEGORIES-'].update(news_categories)
    
    elif event == 'Удалить категорию':
        selected = values['-CATEGORIES-']
        for item in selected:
            news_categories.remove(item)
        window['-CATEGORIES-'].update(news_categories)
    
    elif event == 'Сформировать выгрузку':
        start_date = values['-START_DATE-']
        end_date = values['-END_DATE-']
        file_path = values['-FILE_PATH-']
        
        # Проверка на корректность пути
        if file_path and not file_path.endswith('.xls'):
            sg.popup_error('Пожалуйста, выберите файл с расширением .xls')
        else:
            sg.popup('Данные сохранены!', f'Застройщики: {values["-DEVELOPERS-"]}\n'
                                           f'Категории: {values["-CATEGORIES-"]}\n'
                                           f'Дата начала: {start_date}\n'
                                           f'Дата окончания: {end_date}\n'
                                           f'Файл: {file_path}')
        
window.close()