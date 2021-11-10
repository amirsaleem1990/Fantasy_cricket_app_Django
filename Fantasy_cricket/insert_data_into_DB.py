import sqlite3
from faker import Faker
from random import shuffle
import pandas as pd
from super_user.models import *

# conn = sqlite3.connect("db.sqlite3")
fake = Faker()

# ID = list(range(1,8))
NAME = [f'Country_{i}' for i in range(1,8)]
CREATED_AT =[str(fake.date_time()) for i in range(7)]

for name, created_at in zip(NAME, CREATED_AT):
    Country(name = name, created_at = created_at).save()
# pd.DataFrame({"id"         : ID,
              # "name"       : NAME,
              # "created_at"   : CREATED_AT}).to_sql("country", if_exists="replace", con=conn, index=False)

#-----------------------------------------------------------------

# ID = list(range(100))
NAME = [fake.name() for i in range(100)]

CATEGORY = ['batsman']*25 + ['all_rounder']*25 + ['wicket_keeper']*25 +['bowler']*25
shuffle(CATEGORY)

COUNTRY_ID = sorted((list(range(1,8))*15)[:100])

for name, catagory, country_id in zip(NAME, CATEGORY, COUNTRY_ID):
    Players(country_id = country_id,
            name = name,
            category=catagory).save()

# pd.DataFrame({"id"         : ID,
#               "country_id" : COUNTRY_ID,
#               "name"       : NAME,
#               "category"   : CATEGORY}).to_sql("Players", if_exists="replace", con=conn, index=False)

#-----------------------------------------------------------------
# ID = list(range(1,5))
lst = [
    ['Country_1', 'Country_2', '1980-03-04', '1980-03-04 14:20:51', '0'],
    ['Country_2', 'Country_3', '2021-03-04', '1980-03-04 14:20:51', '0'],
    ['Country_5', 'Country_1', '2021-11-01', '1980-03-04 14:20:51', '0'],
    ['Country_4', 'Country_2', '2022-11-01', '1980-03-04 14:20:51', '1'],
    ['Country_3', 'Country_1', '2021-11-01', '2021-11-01 10:20:00', '0'],
    ['Country_2', 'Country_1', '2021-11-26', '2021-11-01 10:44:00', '0'],
    ['Country_2', 'Country_6', '2021-11-26', '2021-11-01 10:45:00', '0'],
    ['Country_2', 'Country_6', '2021-11-26', '2021-11-01 10:46:00', '1'],
    ['Country_2', 'Country_6', '2021-11-26', '2021-11-01 10:49:00', '0']
    ]

for i in lst:
    Matches(country_1 = i[0], country_2 = i[1] , date = i[2], created_at = i[3], recorded = i[4]).save()

# pd.DataFrame({"id"         : ID,
#               "country_1"  : country_1,
#               "country_2"  : country_2,
#               "date"       : date,
#               "created_at" : created_at}).to_sql("Matches", if_exists="replace", con=conn, index=False)


