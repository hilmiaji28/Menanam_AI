import pandas as pd

padi = pd.read_csv(
    "data/clean/padi_clean.csv"
)

jagung = pd.read_csv(
    "data/clean/jagung_clean.csv"
)

ubi_kayu = pd.read_csv(
    "data/clean/ubi_kayu_clean.csv"
)

crop = pd.concat(
    [padi, jagung, ubi_kayu],
    ignore_index=True
)

crop.to_csv(
    "data/clean/crop_productivity.csv",
    index=False
)

print(crop.shape)