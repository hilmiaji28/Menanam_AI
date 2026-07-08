import pandas as pd

df = pd.read_csv("data/primary/final_dataset_modeling.csv")

print(
    df.groupby("komoditas")["produktivitas"].describe()
)

print()

print(
    df.groupby("komoditas")["produktivitas"].quantile(
        [0.25,0.50,0.75]
    )
)