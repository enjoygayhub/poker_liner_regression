import pandas as pd
import csv
from collections import Counter

data = pd.read_csv('flop0.csv')
features = data[:]
x=features.values
result = []
for i in range(503):
    data=[]
    a=list(x[i])
    lable = a.pop()
    flowers = a[::2]
    nums = a[1::2]

    # c = Counter(nums).most_common(1)
    # pair1=c[0][0]
    data.append(round(max(nums[0],nums[1])/12,3))
    data.append(round(min(nums[0],nums[1])/12,3))

    if max(nums)==nums[0] or max(nums)==nums[1]:
        data.append(1)
    else:
        data.append(0)
    if Counter(flowers).most_common(1)[0][1]==4:
        data.append(1)
    else:
        data.append(0)
    nums.sort()
    if nums[3]-nums[0]==3 or nums[4]-nums[1]==3 :
        data.append(1)
    elif nums[3]-nums[0]==4 or nums[4]-nums[1]==4 :
        data.append(0.5)
    else:
        data.append(0)
    data.append(round(lable,3))
    result.append(data)

with open('file0.csv', 'w', newline='') as t_file:
    csv_writer = csv.writer(t_file)
    for l in result:
        csv_writer.writerow(l)







