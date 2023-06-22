import json
import pandas as pd

# load the excel file to get gpins from
listings = pd.read_excel(r'vabeachlistings.xlsx')

# build dataframe
df = pd.DataFrame(listings, columns=['gpin'])
print("Dataframe built")

# build gpin list
gpins = []
for k in df.index:
    gpins.append(df['gpin'][k])
gpins.sort()
print("GPINS in List")

count = 1

df = pd.DataFrame()
# list for the rows to be added to dataframe
row_list = []

for g in gpins:

    # open the json file with the gpin of g
    with open(r'listingdetails\\' + str(g) +'.json') as details_file:
        data = json.load(details_file)

        # Only get data from properties with one building
        if len(data['data'][0]['buildings']) < 2:
            # Get the appraisal history
            start_year = 2008
            end_year = 2020
            for tax_assessments in data['data'][0]['taxAssessAmts']:
                data_dt = {}
                if end_year >= tax_assessments['taxYear'] >= start_year:
                    print(str(count) + " " + str(g) + ' ' + str(start_year))
                    count += 1
                    # get the property gpin
                    data_dt.update({'gpin': data['data'][0]['gpin']})
                    data_dt.update({'Year': tax_assessments['taxYear']})
                    data_dt.update({'landValue': tax_assessments['landValue']})
                    data_dt.update({'impValue': tax_assessments['improvementValue']})
                    data_dt.update({'assessAmt': tax_assessments['assessAmt']})
                    data_dt.update({'taxRate': tax_assessments['taxRate']})
                    data_dt.update({'taxAmount': tax_assessments['taxAmount']})
                    # monitor progress
                    row_list.append(data_dt)
    details_file.close()
# update dataframe with list
df = pd.DataFrame(row_list)
# write data to excel file
with pd.ExcelWriter(str(start_year) + '_appraisals.xlsx') as writer:
    df.to_excel(writer, index=False)

