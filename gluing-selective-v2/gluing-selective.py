import os
from pathlib import Path

def count_lines(content):
    """Подсчитывает количество строк в тексте."""
    return len(content.splitlines())

def show_files_and_get_selection(files_list):
    """Показывает список файлов и возвращает выбранные номера."""
    print("\nСписок файлов:")
    for i, file_path in enumerate(files_list, 1):
        print(f"{i}. {file_path}")
    
    print("\nВведите номера файлов для склейки (через запятую):")
    selection = input("> ").strip()
    selected_indices = [int(num.strip()) - 1 for num in selection.split(",") if num.strip().isdigit()]
    
    return selected_indices

def glue_selected_files(input_dir, selected_files):
    """Объединяет выбранные файлы в один."""
    # Создаем папку Отчеты, если её нет
    output_dir = "Отчеты"
    Path(output_dir).mkdir(exist_ok=True)
    
    # Получаем имя папки для названия выходного файла
    folder_name = os.path.basename(os.path.normpath(input_dir))
    
    # Собираем содержимое выбранных файлов и считаем строки
    total_lines = 0
    files_content = []
    
    for file_path in selected_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as in_file:
                content = in_file.read()
                lines = count_lines(content)
                total_lines += lines
                files_content.append((file_path, content, lines))
        except (UnicodeDecodeError, PermissionError):
            print(f"Ошибка чтения файла: {file_path}")
            continue
    
    if not files_content:
        print("Нет файлов для объединения!")
        return
    
    # Создаем уникальное имя файла
    index = 0
    while True:
        output_filename = f'Объединенный_отчет_{folder_name}-{total_lines}_({index}).txt'
        output_path = os.path.join(output_dir, output_filename)
        if not os.path.exists(output_path):
            break
        index += 1
    
    # Записываем результат
    with open(output_path, 'w', encoding='utf-8') as out_file:
        for file_path, content, lines in files_content:
            out_file.write(f"=== {file_path} === (строк: {lines})\n")
            out_file.write(content)
            out_file.write("\n" + "-" * 50 + "\n\n")
    
    print(f"\nФайлы объединены в: {output_path}")
    print(f"Всего строк: {total_lines}")

def get_all_files(input_dir):
    """Рекурсивно собирает все файлы в директории."""
    all_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

if __name__ == "__main__":
    print("=== Склейка файлов ===")
    print("Создаст папку 'Отчеты' с объединенным файлом")
    
    # Запрашиваем путь к папке
    while True:
        input_dir = input("\nВведите путь к папке: ").strip()
        if os.path.isdir(input_dir):
            break
        print(f"Ошибка: папка '{input_dir}' не существует!")
    
    # Получаем все файлы и показываем пользователю
    all_files = get_all_files(input_dir)
    if not all_files:
        print("В указанной папке нет файлов!")
        exit()
    
    selected_indices = show_files_and_get_selection(all_files)
    selected_files = [all_files[i] for i in selected_indices if 0 <= i < len(all_files)]
    
    if not selected_files:
        print("Не выбрано ни одного файла!")
        exit()
    
    # Объединяем выбранные файлы
    glue_selected_files(input_dir, selected_files)