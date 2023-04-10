import pandas as pd
from pprint import pprint
import numpy as np


def split_rosanita(n):
    return n.split()[0].lower()


def split_nema(n):
    return n.split("_")[0].lower()


def create_data():
    cp_feeding = pd.read_csv("data/cp+feeding.csv", sep=";")
    nema = pd.read_excel("data/nema_cpanalysis.xlsx")

    init_col = 13
    end_col = 113

    end_row = 50

    bichos = nema.iloc[:end_row, init_col:end_col]

    total_bichos_count = bichos.sum(axis=1)

    sp_feed = cp_feeding["SP "]
    cp_feed = cp_feeding["CP"]

    sp_clean = sp_feed.apply(split_rosanita)
    sp_clean_map = pd.DataFrame({"SP": sp_clean, "CP": cp_feed})

    sp_unique_map = sp_clean_map.drop_duplicates(subset=["SP"], keep="first")

    global_cp_counter = {cp: [] for cp in sp_unique_map["CP"].unique()}
    for i, row in bichos.iterrows():
        row_cp_counter = {cp: [] for cp in sp_unique_map["CP"].unique()}
        for col in bichos.columns:
            clean_col = split_nema(col)

            current_cp = sp_unique_map[sp_unique_map["SP"] == clean_col]["CP"]

            if len(current_cp.values) <= 0:
                print(clean_col, col, current_cp)
                continue
            else:
                row_cp_counter[current_cp.values[0]].append(row[col])

        for k, v in row_cp_counter.items():
            global_cp_counter[k].append(v)

    # print(global_cp_counter[4])

    master_counter = {cp: [] for cp in sp_unique_map["CP"].unique()}
    for k, v in global_cp_counter.items():
        np_arr = np.array(v)
        sum = np_arr.sum(axis=1)
        master_counter[k] = sum

    master_counter["total"] = total_bichos_count.values

    output = pd.DataFrame(master_counter, dtype=int)
    output.to_csv("cp_per_sample.csv", index=False)
    print(pd.DataFrame(master_counter, dtype=int))


if __name__ == "__main__":
    create_data()
