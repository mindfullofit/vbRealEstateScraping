import requests
import time

# Select what page to start on. Pagination used draw to label page
draw = 1
# Start of page listing
start = (draw - 1) * 10
# Which house to start on
startIndex = start + 1

while draw < 3:
    p = {
        'draw':draw,'columns%5B0%5D%5Bdata%5D':'gpin',
        "columns%5B0%5D%5Bname%5D":'',
        "columns%5B0%5D%5Bsearchable%5D":"true",
        "columns%5B0%5D%5Borderable%5D":"false",
        "columns%5B0%5D%5Bsearch%5D%5Bvalue%5D":"",
        "columns%5B0%5D%5Bsearch%5D%5Bregex%5D":"false",
        "columns%5B1%5D%5Bdata%5D":"situsStreet",
        "columns%5B1%5D%5Bname%5D":"",
        "columns%5B1%5D%5Bsearchable%5D":"true",
        "columns%5B1%5D%5Borderable%5D":"false",
        "columns%5B1%5D%5Bsearch%5D%5Bvalue%5D":"",
        "columns%5B1%5D%5Bsearch%5D%5Bregex%5D":"false",
        "columns%5B2%5D%5Bdata%5D":"neighName",
        "columns%5B2%5D%5Bname%5D":"",
        "columns%5B2%5D%5Bsearchable%5D":"true",
        "columns%5B2%5D%5Borderable%5D":"false",
        "columns%5B2%5D%5Bsearch%5D%5Bvalue%5D":"",
        "columns%5B2%5D%5Bsearch%5D%5Bregex%5D":"false",
        "columns%5B3%5D%5Bdata%5D":"zip",
        "columns%5B3%5D%5Bname%5D":"",
        "columns%5B3%5D%5Bsearchable%5D":"true",
        "columns%5B3%5D%5Borderable%5D":"false",
        "columns%5B3%5D%5Bsearch%5D%5Bvalue%5D":"",
        "columns%5B3%5D%5Bsearch%5D%5Bregex%5D":"false",
        "start":start,
        "length":10,
        "search%5Bvalue%5D":"",
        "search%5Bregex%5D":"false",
        "SearchType":"property",
        "OccupancyStatus":"Occupied",
        "PropertyType":"Residential",
        "MaxRows":10,
        "Request":"GetPropertyResult",
        "StartIndex":startIndex,
        "_":1603946025526}
    receive = requests.get("https://www.vbgov.com/_assets/apps/property-search/api/connect.ashx", params=p)
    # print(receive.url)
    #with open(r'C:\Users\itsupport\vabeachresidences\basiclistings\listing'+str(draw)+'.json', 'wb') as f:
    with open(r'D:vbresidences\listing'+str(draw)+'.json', 'wb') as f:
        f.write(receive.content)
        f.close()
    # time.sleep(2)
    draw += 1
    start += 10
    startIndex += 10

print("Done")
