import numpy as np
import pandas as pd

cities = pd.read_csv('city.csv')

#address	postal_code	country	federal_district	region_type	region	area_type	area	city_type	city	
#settlement_type	settlement	kladr_id	fias_id	fias_level	capital_marker	okato	oktmo	tax_office	
#timezone	geo_lat	geo_lon	population	foundation_year


cities.drop(['city', 'country', 'federal_district', 'region_type', 'region', 'area_type', 'area', 'city_type', 'postal_code', 'timezone', 'foundation_year'], axis=1, inplace=True)
cities.drop(['settlement_type', 'settlement', 'kladr_id', 'fias_id', 'fias_level', 'capital_marker', 'okato', 'oktmo', 'tax_office'], axis=1, inplace=True)

cities = cities.sort_values(by="population", ascending=[0])

def get_city(s):
    s = s[::-1] 
    t = s[ : s.find(' г')]
    t = t[::-1]
    return t

cities.drop(['population',], axis=1, inplace=True)

cities['address'] = cities['address'].apply(get_city)
cities = cities.head(30)

print(cities.to_string())

#cities = cities.to_csv('top-30_cities.csv', index=False)