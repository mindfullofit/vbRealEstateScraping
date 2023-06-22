import json
import pandas as pd
from os.path import exists

filePath = "D:/vbresidences/listing";
df = pd.DataFrame(columns=("gpin", "situsStreet", "neighName", "zip"))
# start with an empty list
rows_list = []
startPage = 1
maxPage = 14864
while startPage <= maxPage:
    if exists(filePath + str(startPage) + '.json'):
        with open(filePath + str(startPage) + '.json') as f:
            data = json.load(f)
            for d in data['data']:
                # new dictionary
                dt1 = {}
                # add the data
                dt1.update({'gpin': d["gpin"]})
                dt1.update({'situsStreet': d["situsStreet"]})
                dt1.update({'neighName': d["neighName"]})
                dt1.update({'zip': d['zip']})
                # append dictionary to list
                rows_list.append(dt1)
        # close file
        f.close()
    # update for sentinel
    startPage += 1
    print(startPage)

# update dataframe with list
df = pd.DataFrame(rows_list)
# write data to excel file
with pd.ExcelWriter(filePath+'/vabeachlistings.xlsx') as writer:
    df.to_excel(writer, index=False)
