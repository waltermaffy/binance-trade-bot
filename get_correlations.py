import urllib.request, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import json
import os

"""
def get_correlations():    
    correlation_file = "correl.json"
    if os.path.exists(correlation_file):
        with open(correlation_file, "r") as f:
            data = json.load(f)
    else:
        with urllib.request.urlopen("https://www.cyrii.com/api/get_correlations_bf/") as url:
            data = json.loads(url.read().decode())
        with open(correlation_file, "w") as f:
            json.dump(data, f)
    return data


data = get_correlations()

correl = {}

for d in data["dataset"][0]["data"]:
    to = d["rowid"]
    fr = d["columnid"]
    value = d["value"]
    correl[(to, fr)] = value
    correl[(fr, to)] = value

coins_file = './supported_coin_list'
with open(coins_file, "r") as f:
    coin_list = sorted(f.read().splitlines())[1:]

ncoin = len(coin_list)

mat = np.ones((ncoin, ncoin))
for i in range(ncoin):
    for j in range(ncoin):
        pair = (coin_list[i], coin_list[j])
        if pair in correl:
            mat[i, j] = correl[pair]


cdict = {'red':   ((0.0, 0.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),
         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),
         'green': ((0.0, 0.0, 0.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 1.0, 1.0))}

cmap = mcolors.LinearSegmentedColormap(
'my_colormap', cdict, 100)

fig, ax = plt.subplots()
plt.imshow(np.log(mat+1)-1, cmap=cmap)
ax.set_xticks(range(ncoin))
ax.set_yticks(range(ncoin))
ax.set_xticklabels(coin_list)
ax.set_yticklabels(coin_list)
fig, ax = plt.subplots()

avg_correl = np.mean(mat, -1)

names, vals = zip(*sorted([(n, v) for n, v in zip(coin_list, avg_correl) if v < 1], key=lambda x: x[1], reverse=True))
nplt = len(names)
plt.bar(range(nplt), vals)
ax.set_xticks(range(nplt))
ax.set_xticklabels(names)
plt.savefig('correlations.jpg')
plt.show()
"""

coins_file = './supported_coin_list'
with open(coins_file, "r") as f:
    coin_list = sorted(f.read().splitlines())[1:]

corr = ''
for c in coin_list:
    corr += f'{c}.CC,'
corr = corr[:-1]
print(corr[:-1])
url = f'https://www.macroaxis.com/invest/marketCorrelation?s={corr}&ot=cloud&mode=i'
#print(url)
with urllib.request.urlopen(url) as u:
    data = u.read().decode('utf-8')
    with open('./correlations.html', "w") as f:
        f.write(data)