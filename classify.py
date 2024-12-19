import pandas as pd
from transformers import pipeline

# Инициализация языковой модели
model = pipeline(model="facebook/bart-large-mnli")

# Функция для присвоения темы заголовку
def assign_topics(row, topics, progress_bar, current_index, total_rows):
    result = model(row['header'], topics)
    assigned_topics = []
    if result['scores'][0] > 0.6:
        assigned_topics.append(result['labels'][0])
    if len(topics) >= 2:
        if result['scores'][1] > 0.6:
            assigned_topics.append(result['labels'][1])
    if len(topics) >= 3:
        if result['scores'][2] > 0.6:
            assigned_topics.append(result['labels'][2])
    
    progress_bar.update(round(current_index / total_rows * 100))
    
    return pd.Series({
            topic: row['header'] if topic in assigned_topics else None
            for topic in topics
        })

def set_topics(data, topics, progress_bar):
    total_rows = len(data)
    data[topics] = data.apply(
        lambda row: assign_topics(row, topics, progress_bar, int(row.name), total_rows),
        axis=1,
    )
    data = data.dropna(subset=topics, how='all')
    return data
    