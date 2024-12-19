import json
import pandas as pd
import PySimpleGUI as sg

from prepare_data import get_data
from classify import set_topics

ALLOWED_DEVELOPERS = ["ПИК", "ЛСР", "ФСК", "Донстрой"]
DEVELOPERS_LINKS = {
    'ПИК': 'https://www.pik.ru',
    'ЛСР': 'https://www.lsr.ru/msk',
    'ФСК': 'https://fsk.ru',
    'Донстрой': 'https://donstroy.moscow/',
}

with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Передача значений в переменные
developers = data['developers']
news_categories = data['news_categories']

sg.theme('LightBrown1')

# Функция для создания окна
def create_window():
    layout = [
        [sg.Text('Выберите застройщиков')],
        [sg.Listbox(developers, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(30, 4), key='-DEVELOPERS-')],
        [sg.Button('Добавить застройщика'), sg.Button('Удалить застройщика')],
        
        [sg.Text('Выберите категории новостей')],
        [sg.Listbox(news_categories, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(30, 5), key='-CATEGORIES-')],
        [sg.Button('Добавить категорию'), sg.Button('Удалить категорию')],
        
        [sg.Text('Дата начала:'), sg.Input(key='-START_DATE-', size=(10, 1)), sg.CalendarButton('Выбрать', target='-START_DATE-', format='%Y-%m-%d')],
        [sg.Text('Дата окончания:'), sg.Input(key='-END_DATE-', size=(10, 1)), sg.CalendarButton('Выбрать', target='-END_DATE-', format='%Y-%m-%d')],
        
        [sg.Text('Выберите путь к выходному файлу (.xls):'), sg.Input(key='-FILE_PATH-', size=(25, 1)), sg.FileSaveAs('Обзор', file_types=(('Excel Files', '*.xls'),))],
        
        [sg.Button('Сформировать выгрузку'), sg.Button('Выход')],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-', visible=False)],
    ]
    
    return sg.Window('Парсинг новостей', layout)

# Основной цикл
window = create_window()
while True:
    event, values = window.read()
    
    if event in (sg.WINDOW_CLOSED, 'Выход'):
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump({
                    'developers': developers, 
                    'news_categories': news_categories, 
                }, 
                file, 
                ensure_ascii=False, 
                indent=4
            )
        break
    
    elif event == 'Добавить застройщика':
        new_developer = sg.popup_get_text('Введите имя застройщика:')
        if new_developer and new_developer in ALLOWED_DEVELOPERS:
            developers.append(new_developer)
            window['-DEVELOPERS-'].update(developers)
        else:
            sg.popup('Пока не поддерживается парсинг новостей данного застройщика')
    
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
        
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump({
                    'developers': developers, 
                    'news_categories': news_categories, 
                }, 
                file, 
                ensure_ascii=False, 
                indent=4
            )
        
        # Проверка на корректность пути
        if file_path and not file_path.endswith('.xls'):
            sg.popup_error('Пожалуйста, выберите файл с расширением .xls')
        elif len(developers) == 0:
            sg.popup_error('Необходимо выбрать хотя бы одного застройщика')
        elif len(news_categories) == 0:
            sg.popup_error('Необходимо выбрать хотя бы одну тему новостей')
        elif end_date < start_date and end_date != '' and start_date != '':
            sg.popup_error('Дата окончания не может быть меньше даты начала')
        else:
            selected_developers = values['-DEVELOPERS-']
            selected_topics = values['-CATEGORIES-']
            
            window['-PROGRESS-'].update(0)  # Сброс прогресс-бара
            window['-PROGRESS-'].update(visible=True) # Делаем прогресс-бар видимым
            
            if not file_path:
                file_path = 'out.xls'
            
            data = get_data(selected_developers, start_date, end_date)
            data['Сайт'] = data['developer_name'].map(DEVELOPERS_LINKS)
            data.reset_index(drop=True, inplace=True)
            data = set_topics(data, selected_topics, window['-PROGRESS-'])
            data.reset_index(drop=True, inplace=True)
            
            
            data_to_write = data[['developer_name', 'Сайт'] + selected_topics]
            data_to_write.rename(columns={
                'developer_name': 'Застройщик',
            }, inplace=True)
            
            
            with pd.ExcelWriter(file_path, mode='w', engine='xlsxwriter') as writer:
                data_to_write.to_excel(writer, sheet_name='Sheet1', index=True)

                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
            
                for i in range(len(data)):
                    worksheet.write_url(i + 1, 2, data_to_write.iloc[i, 1], string=data_to_write.iloc[i, 1])
                    for t, topic in enumerate(selected_topics):
                        if not pd.isna(data[topic].iloc[i]):
                            worksheet.write_url(i + 1, 2+t+1, data.iloc[i, 1], string=data.iloc[i, 3])
            
            window['-PROGRESS-'].update(visible=False)
            sg.popup('Выгрузка сформирована!', f'Застройщики: {values["-DEVELOPERS-"]}\n'
                                           f'Категории: {values["-CATEGORIES-"]}\n'
                                           f'Дата начала: {start_date}\n'
                                           f'Дата окончания: {end_date}\n'
                                           f'Файл: {file_path}'
                )
        
window.close()