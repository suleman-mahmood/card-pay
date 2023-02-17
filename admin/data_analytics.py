import pandas as pd
import json


with open("2023-02-17 07-31-32_DBState.json") as f:
    data = json.load(f)

df = pd.DataFrame.from_dict(data["transactions"], "index")
df.drop(["recipientId", "id", "senderId"], axis=1, inplace=True)
df.to_csv("data.csv")

# sum = df[df["recipientName"] == "Bunkers"]["amount"].sum()
# print(sum)
