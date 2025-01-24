import pandas as pd

EXCEL_FILE = "BI_Lab1_data_source.xlsx"


def load_books_data_from_excel(excel_file=EXCEL_FILE, sheet_name=0):
    """
    Зчитує дані з одного Excel-файлу (аркуш sheet_name).
    Повертає DataFrame з потрібними колонками (RatingDist1..5, Rating, і т.д.).
    """
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # 1) Замінимо кому на крапку в Rating (наприклад, "4,57" -> "4.57" -> float).
    if 'Rating' in df.columns:
        df['Rating'] = (df['Rating'].astype(str)
                        .str.replace(",", ".", regex=False)
                        .astype(float))

    # 2) Приведемо числові колонки до int/float
    numeric_cols = [
        "RatingDist1", "RatingDist2", "RatingDist3",
        "RatingDist4", "RatingDist5", "CountsOfReview",
        "PublishDay", "PublishMonth", "PublishYear"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3) Створимо RatingDistTotal, якщо його немає
    if "RatingDistTotal" not in df.columns:
        df["RatingDistTotal"] = df[["RatingDist1", "RatingDist2",
                                    "RatingDist3", "RatingDist4",
                                    "RatingDist5"]].sum(axis=1)

    return df


# -----------------------------
# 1. Завантаження даних
# -----------------------------
books_df = load_books_data_from_excel(EXCEL_FILE)
print("Загальні колонки:", books_df.columns.tolist())
print("Перші рядки:\n", books_df.head())

# -----------------------------
# 2. Приклад створення Pivot-таблиць у pandas
# -----------------------------

# Pivot A: Середній рейтинг (Rating) за роком публікації (PublishYear) та мовою (Language)
pivot_rating_year_language = pd.pivot_table(
    data=books_df,
    values='Rating',
    index='PublishYear',
    columns='Language',
    aggfunc='mean'
)
print("\nPivot A: Середній рейтинг (mean) за PublishYear x Language:\n", pivot_rating_year_language.head())
pivot_rating_year_language.to_csv("pivot_rating_year_language.csv", index=True)

# Pivot B: Кількість рецензій (CountsOfReview) за видавцем (Publisher) та роком
if "CountsOfReview" in books_df.columns:
    pivot_reviews_pub_year = pd.pivot_table(
        data=books_df,
        values='CountsOfReview',
        index='Publisher',
        columns='PublishYear',
        aggfunc='sum'
    ).fillna(0)
    print("\nPivot B: Сума CountsOfReview за Publisher x PublishYear:\n", pivot_reviews_pub_year.head())
    pivot_reviews_pub_year.to_csv("pivot_reviews_pub_year.csv", index=True)

# Pivot C: Сума RatingDistTotal (кількість оцінок) по (Language) і (PublishYear)
if "RatingDistTotal" in books_df.columns:
    pivot_rdist_lang_year = pd.pivot_table(
        data=books_df,
        values='RatingDistTotal',
        index='Language',
        columns='PublishYear',
        aggfunc='sum'
    ).fillna(0)
    print("\nPivot C: Сумарна RatingDistTotal за Language x PublishYear:\n", pivot_rdist_lang_year.head())
    pivot_rdist_lang_year.to_csv("pivot_rdist_lang_year.csv", index=True)

# Додатково створимо поле для (Year-Month)
books_df['PublishYearMonth'] = books_df['PublishYear'].astype(str) + "-" + books_df['PublishMonth'].astype(str)
pivot_rating_month = pd.pivot_table(
    data=books_df,
    values='Rating',
    index='PublishYearMonth',
    aggfunc='mean'
).sort_index()
print("\nPivot D: Середній рейтинг (mean) за PublishYearMonth:\n", pivot_rating_month.head())
pivot_rating_month.to_csv("pivot_rating_yearmonth.csv", index=True)

print("\n--- ЗВЕДЕНІ ТАБЛИЦІ СТВОРЕНО ТА ЗБЕРЕЖЕНО У CSV ---")
