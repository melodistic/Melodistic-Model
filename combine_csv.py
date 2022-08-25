import pandas as pd
import os
file_list = os.listdir('csv_data')
data = []
for file in file_list:
    data.append(pd.read_csv('csv_data/' + file))

df = pd.concat(data)
df.to_csv('music.csv', index=False)