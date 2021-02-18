
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('../data/model_128x4_64_64_2.csv', index_col=None)
#df = pd.read_csv('../data/model_20x5_30x4_42_7_2.csv', index_col=None)
df.columns = ['agent', 'rate']
df['x100'] = range(0, len(df))

plt.figure(figsize=(14,6))
fig = sns.lineplot(df.x100, df.rate, hue=df.agent)
fig.set(xlabel='Number of games x100', ylabel='Winning rate')
fig.set(ylim=(0, 1))
plt.show()
