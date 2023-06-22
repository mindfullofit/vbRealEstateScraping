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
        data_dt = {}
        # Is there only one building on the property
        buildingCount = len(data['data'][0]['buildings'])

        if buildingCount == 1:
            # Make sure a dwelling is present on the property
            use_codes = []
            # find improvements
            for improvements in data['data'][0]['buildings'][0]['improvements']:
                use_codes.append(improvements['useCode'])
            dwelling_code = "DWELL" in use_codes
            if dwelling_code == True:
                # get the general data
                data_dt.update({'gpin': data['data'][0]['gpin']})
                data_dt.update({'neighName': data['data'][0]['neighName']})
                data_dt.update({'situsStreet': data['data'][0]['situsStreet']})
                data_dt.update({'zip': data['data'][0]['zip']})
                data_dt.update({'district': data['data'][0]['district']})
                data_dt.update({'classCode': data['data'][0]['classCode']})
                data_dt.update({'classCdDesc': data['data'][0]['classCdDesc']})
                # get geo information
                data_dt.update({'longitude': data['data'][0]['longitude']})
                data_dt.update({'latitude': data['data'][0]['latitude']})
                # land use info
                data_dt.update({'landUse': data['data'][0]['landUse']})
                data_dt.update({'landUseYN': data['data'][0]['landUseYN']})
                data_dt.update({'closestParkDistance': data['data'][0]['closestParkDistance']})

                # Get the building details
                for b in data['data'][0]['buildings']:
                    # Get the square footage of each level
                    for sq in b['squareFootages']:
                        # add floor sqft: Here, floor key is dynamically allocated
                        if sq['floorKey'] == "Total":
                            data_dt.update({'floorKeyTotalSqFt': sq['totalSqFt']})
                    # get the dwelling data
                    for dw in b['dwellings']:
                        data_dt.update({'halfBaths': dw['halfBaths']})
                        data_dt.update({'fullBaths': dw['fullBaths']})
                        data_dt.update({'totalRooms': dw['totalRooms']})
                        data_dt.update({'cooling': dw['cooling']})
                        data_dt.update({'heating': dw['heating']})
                        data_dt.update({'bedRooms': dw['bedRooms']})
                    # find exterior features
                    for extfeatures in b['extFeatures']:
                        if extfeatures['extFeatCode'] == 'CONCP':
                            data_dt.update({extfeatures['extFeatDesc']: 1})
                    # find improvements
                    for improvements in b['improvements']:
                        improvement_list = ['ATTGAR', 'DETGAR', 'POOL', 'DWELL']
                        if improvements['useCode'] in improvement_list:
                            if improvements['useCode'] == 'DWELL':
                                data_dt.update({'YearBuilt': improvements['constrYr']})
                            else:
                                data_dt.update({improvements['description']: 1})

                # Get the land details
                acres = 0;
                for ld in data['data'][0]['landDetails']:
                    acres = ld['landAcres'] + acres
                # Calculate Total land acreage in square feet
                data_dt.update({'totalLotSizeSqFt': acres * 43560})

                row_list.append(data_dt)
        details_file.close()

    # monitor progress
    print(str(count) + " " + str(g))
    count += 1

# update dataframe with list
df = pd.DataFrame(row_list)
# write data to excel file
with pd.ExcelWriter('propertydetails_with_coordinates.xlsx') as writer:
    df.to_excel(writer, index=False)
