import pandas as pd
import time
import random

df = pd.read_csv("netflix_titles.csv")
chunk_size = 1000

for x in range(10):
    for i in range(0, len(df), chunk_size):
        chunk = df[i:i + chunk_size]
        chunk.to_csv(f"stream-input/part_{x}-{i}.csv", index=False)
        print(f"Wrote part_{i}.csv")
        time.sleep(1)