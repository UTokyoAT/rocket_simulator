import pandas as pd
import matplotlib.pyplot as plt

t = pd.read_csv('time.csv')
t = t[t["cpu"] > 1.5e6]
print(t.head())
plt.hist(t['real'], bins=20)
plt.hist(t['cpu'], bins=20, alpha=0.5)
plt.show()