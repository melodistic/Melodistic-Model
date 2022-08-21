import pandas as pd
df = pd.concat(map(pd.read_csv, [str(i)+".csv" for i in range(20)]), ignore_index=True)
df.to_csv("music.csv", index=False, header=True)