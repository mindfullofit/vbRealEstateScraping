import concurrent.futures
import requests
import pandas as pd
import urllib.parse as urlparse
from urllib.parse import parse_qs


def build_url(gpins):
    urls = []
    url = 'https://www.vbgov.com/_assets/apps/property-search/api/connect.ashx?Request=GetPropertyDetail&gpin='
    for gpin in gpins:
        urls.append(url + str(gpin))
    return urls

# Retrieve a single page and return the contents
def load_url(url):
    receive = requests.get(url)
    return receive.content


# load the excel file
listings = pd.read_excel(r'D:\vbresidences\listing\vabeachlistings.xlsx')
df = pd.DataFrame(listings, columns=['gpin'])

print("Dataframe built")
# build gpin list
gpins = []
for k in df.index:
    gpins.append(df['gpin'][k])
print("GPINS in List")
# build the urls
URLS = build_url(gpins)
print("URLS built")

# empty list
row_list = []

count = 1
# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        parsed = urlparse.urlparse(url)
        localgpin = parse_qs(parsed.query)['gpin']
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            # add to list
            row_list.append(data)
            print(count)
            count += 1
            with open(r'D:\vbresidences\listing\details\\' + localgpin[0] + '.json', 'wb') as f:
                f.write(data)
                f.close()

print("All done")
