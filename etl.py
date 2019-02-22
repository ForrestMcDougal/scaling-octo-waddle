import time

import pymongo
import pandas as pd

import scrape_land
import zip_county
import get_weather

# initiate MongoDB databse with name `landDB`
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.landDB

# comment out this next line to append data
# use only if you want to start new
db.farms.remove({})

# choose number of pages to scrape
pages_to_scrape = 1

df = pd.read_csv('https://query.data.world/s/d4svu353zh227c66s7tix7gav44gkz')
df.rename(columns={'ZCTA5': 'Zipcode'}, inplace=True)
df.set_index("Zipcode")

for i in range(1, pages_to_scrape + 1):
    url = f'https://www.landsofamerica.com/United-States/farms/page-{i}'
    div_tops = scrape_land.get_all_land(url)
    for div_top in div_tops:
        time.sleep(1)
        try:
            land_info = scrape_land.scrape_land(div_top)
            zip_code = int(land_info['postal_code'])
            try:
                land_info['weather_info'] = get_weather.get_weather(zip_code)
            except:
                pass
            try:
                zip_data = zip_county.getZipCounty(zip_code, df)
                if zip_data:
                    land_info['zip_data'] = zip_data
            except:
                pass
            db.farms.insert_one(land_info)
        except:
            pass
