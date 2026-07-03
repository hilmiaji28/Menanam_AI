import pandas as pd

input_file = "data/raw/FAOSTAT_data_en_6-18-2026.csv"
output_file = "data/clean/fao_ml.csv"

df = pd.read_csv(input_file)

df_ml = df.pivot_table(
    index=["Year", "Item"],
    columns="Element",
    values="Value",
    aggfunc="first"
).reset_index()

df_ml.columns.name = None

print(df_ml.head())

df_ml.to_csv(output_file, index=False)

print("\n====================")
print("TRANSFORMATION COMPLETE")
print("====================")
print(f"Rows : {len(df_ml):,}")
print(f"File : {output_file}")