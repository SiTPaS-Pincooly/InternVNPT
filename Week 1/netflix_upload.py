import pandas as pd

df = pd.read_csv(r"C:\Users\Acer Nitro\Downloads\netflix_titles.csv")

print(df.head())
print(len(df))

from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:a-1 b-2 c-3@localhost:3306/kaggle_practice")

df.to_sql(
    name="netflix_titles",
    con=engine,
    if_exists="replace",
    index=False
)
