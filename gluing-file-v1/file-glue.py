import os
from pathlib import Path

def count_lines(content):
    return len(content.splitlines())

def glue_files(input_dir):
    # Создаем папку results, если её нет
    output_dir = "results"
    Path(output_dir).mkdir(exist_ok=True)
    
    # Получаем имя папки для названия выходного файла
    folder_name = os.path.basename(os.path.normpath(input_dir))
    
    # Собираем содержимое всех файлов и считаем общее количество строк
    total_lines = 0
    files_content = []
    
    # Рекурсивно собираем все файлы
    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as in_file:
                    content = in_file.read()
                    lines = count_lines(content)
                    total_lines += lines
                    files_content.append((file_path, content, lines))
            except (UnicodeDecodeError, PermissionError):
                continue
    
    # Определяем индекс для нового файла
    index = 0
    while True:
        output_filename = f'file-glue_{folder_name}-{total_lines}_({index}).txt'
        output_path = os.path.join(output_dir, output_filename)
        if not os.path.exists(output_path):
            break
        index += 1
    
    # Записываем содержимое в выходной файл
    with open(output_path, 'w', encoding='utf-8') as out_file:
        for file_path, content, lines in files_content:
            out_file.write(f"=== {file_path} === (строк: {lines})\n")
            out_file.write(content)
            out_file.write("\n" + "-" * 10 + "\n\n")
    
    print(f"\nФайлы объединены в: {output_path}")
    print(f"Всего строк: {total_lines}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("File Glue - объединение файлов из папки")
        input_dir = input("Введите путь к папке: ").strip()
        
        # Проверяем существует ли папка
        while not os.path.isdir(input_dir):
            print(f"Ошибка: папка '{input_dir}' не существует!")
            input_dir = input("Введите правильный путь к папке: ").strip()
    else:
        input_dir = sys.argv[1]
    
    glue_files(input_dir)