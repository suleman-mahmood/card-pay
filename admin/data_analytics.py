import pandas as pd
import numpy as np
import json


with open("2022-12-02 19:16:18_DBState.json") as f:
    data = json.load(f)

df = pd.DataFrame.from_dict(data["transactions"], "index")
df.drop(["recipientId", "id", "senderId"], axis=1, inplace=True)
print(df.columns)
df.to_csv("data.csv")

# sum = df[df["recipientName"] == "Bunkers"]["amount"].sum()
# print(sum)
