import pandas as pd
from deep_translator import GoogleTranslator
import csv

# Путь к файлу
input_file_path = 'vk_text.csv'
output_file_path = 'translated_vk_text.csv'

# Чтение исходного файла
df = pd.read_csv(input_file_path)

# Функция для перевода текста
def translate_text(text):
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    except Exception as e:
        print(f"Error translating text: {e}")
        return text

# Создаем новый файл и записываем заголовки
with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'Post text'])

# Перевод и запись данных порциями по 100 строк
batch_size = 2
num_batches = len(df) // batch_size + (1 if len(df) % batch_size != 0 else 0)

for i in range(num_batches):
    batch_df = df.iloc[i * batch_size: (i + 1) * batch_size]
    batch_df['Post text'] = batch_df['Post text'].apply(translate_text)
    batch_df.to_csv(output_file_path, mode='a', header=False, index=False)

print("Translation completed and saved to new CSV file.")