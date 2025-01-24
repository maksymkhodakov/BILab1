import os
import pandas as pd
import numpy as np

# Шлях до папки, де лежать файли
DATA_FOLDER = "/Users/maksymkhodakov/BIProjectLab1/BIProjectLab1/archive"

# "Еталонний" порядок колонок
STANDARD_COLUMNS = [
    "Id", "Name", "Authors", "ISBN", "Publisher",
    "PublishYear", "PublishMonth", "PublishDay",
    "Language", "pagesNumber",
    "Rating", "RatingDistTotal", "RatingDist1",
    "RatingDist2", "RatingDist3", "RatingDist4",
    "RatingDist5", "CountsOfReview"
]


def load_books_data(data_folder=DATA_FOLDER):
    """
    Функція для пошуку і зчитування всіх CSV-файлів із назвою book...csv
    Повертає єдиний DataFrame з уніфікованими колонками STANDARD_COLUMNS
    """
    # 1. Знаходимо всі файли, що починаються на 'book' та закінчуються .csv
    all_files = [
        f for f in os.listdir(data_folder)
        if f.startswith("book") and f.endswith(".csv")
    ]

    df_list = []

    for file_name in all_files:
        file_path = os.path.join(data_folder, file_name)
        print(f"Loading {file_path}...")

        # 2. Зчитуємо CSV
        #    on_bad_lines='skip' – щоб пропустити проблемні рядки (за потреби)
        tmp_df = pd.read_csv(file_path, on_bad_lines='skip', low_memory=False)

        # 3. Визначимо, які колонки є у файлі, а які відсутні
        existing_cols = tmp_df.columns

        # 4. Додамо відсутні колонки як NaN, щоб можна було впорядкувати
        for col in STANDARD_COLUMNS:
            if col not in existing_cols:
                tmp_df[col] = np.nan

        # 5. Тепер впорядковуємо колонки строго за STANDARD_COLUMNS
        tmp_df = tmp_df[STANDARD_COLUMNS]

        # 6. Додаємо цей DataFrame до списку
        df_list.append(tmp_df)

    if len(df_list) == 0:
        print("No book CSV files found!")
        return pd.DataFrame(columns=STANDARD_COLUMNS)

    # 7. Об'єднуємо всі CSV в один DataFrame
    all_books_df = pd.concat(df_list, ignore_index=True)
    print(f"Total rows in all_books_df: {len(all_books_df)}")

    # Додаткові кроки з очищення, якщо треба:
    # - Видалення дублікатів
    # - Перетворення типів (PublishYear -> int, pagesNumber -> int і т.д.)

    return all_books_df


def load_user_ratings(data_folder=DATA_FOLDER):
    # Визначимо бажані колонки (будемо перейменовувати з ID -> UserID, ...)
    rename_map = {
        "ID": "UserID",
        "Name": "SomeName",
        "Rating": "UserRating"
    }

    all_files = [
        f for f in os.listdir(data_folder)
        if f.startswith("user_rating_") and f.endswith(".csv")
    ]

    df_list = []
    for file_name in all_files:
        file_path = os.path.join(data_folder, file_name)
        print(f"Loading {file_path}...")

        tmp_df = pd.read_csv(file_path, on_bad_lines='skip', low_memory=False)

        # Перейменовуємо
        tmp_df = tmp_df.rename(columns=rename_map)

        # Якщо раптом бракує якихось колонок - додаємо
        for col in rename_map.values():
            if col not in tmp_df.columns:
                tmp_df[col] = np.nan

        # Залишимо тільки три колонки
        tmp_df = tmp_df[list(rename_map.values())]

        df_list.append(tmp_df)

    if len(df_list) == 0:
        print("No user_rating_ CSV files found!")
        return pd.DataFrame(columns=list(rename_map.values()))

    all_user_ratings_df = pd.concat(df_list, ignore_index=True)

    print(f"Total rows in all_user_ratings_df: {len(all_user_ratings_df)}")
    return all_user_ratings_df


# Викликаємо
user_ratings_df = load_user_ratings(DATA_FOLDER)
print("Final user_ratings_df columns:", user_ratings_df.columns.tolist())
print(user_ratings_df.head())

# Викликаємо функцію
books_df = load_books_data(DATA_FOLDER)
print("Final books_df columns:", books_df.columns.tolist())
print(books_df.head())
