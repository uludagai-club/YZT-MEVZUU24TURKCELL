import pandas as pd


df_parquet = pd.read_parquet('docs/train/ib_dataset/test_final.parquet/test_final.parquet')

print(df_parquet.head(1))
print("a")
