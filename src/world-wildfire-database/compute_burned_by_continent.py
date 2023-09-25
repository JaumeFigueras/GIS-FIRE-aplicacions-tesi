#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import country_converter as coco
import logging


cc = coco.CountryConverter()
coco_logger = coco.logging.getLogger()
coco_logger.setLevel(logging.FATAL)
burned_area = pd.read_csv('./burned_area.csv')
burned_countries = burned_area.groupby('country').agg({'forest': 'sum', 'savannas': 'sum',
                                                       'shrublands_grasslands': 'sum', 'croplands': 'sum',
                                                       'other': 'sum'}).reset_index()
burned_countries['total_burned_surface'] = (burned_countries['forest'] + burned_countries['savannas'] +
                                            burned_countries['shrublands_grasslands'] + burned_countries['croplands'] +
                                            burned_countries['other'])
burned_countries['continent'] = ''
for i in range(len(burned_countries.index)):
    if burned_countries.at[i, 'country'] == 'Akrotiri and Dhekelia':
        burned_countries.at[i, 'continent'] = 'Asia'
    else:
        burned_countries.at[i, 'continent'] = cc.convert(burned_countries.at[i, 'country'], to='Continent', not_found='Other')
    i += 1


burned_continents = (burned_countries.groupby('continent').agg({'forest': 'sum', 'savannas': 'sum',
                                                               'shrublands_grasslands': 'sum', 'croplands': 'sum',
                                                               'other': 'sum', 'total_burned_surface': 'sum'})
                     .reset_index())

burned_countries_year = burned_area.groupby(['country', 'year']).agg({'forest': 'sum', 'savannas': 'sum',
                                                       'shrublands_grasslands': 'sum', 'croplands': 'sum',
                                                       'other': 'sum'}).reset_index()
burned_countries_year['total_burned_surface'] = (burned_countries_year['forest'] + burned_countries_year['savannas'] +
                                            burned_countries_year['shrublands_grasslands'] + burned_countries_year['croplands'] +
                                            burned_countries_year['other'])

burned_countries_year['continent'] = ''
for i in range(len(burned_countries_year.index)):
    if burned_countries_year.at[i, 'country'] == 'Akrotiri and Dhekelia':
        burned_countries_year.at[i, 'continent'] = 'Asia'
    else:
        burned_countries_year.at[i, 'continent'] = cc.convert(burned_countries_year.at[i, 'country'], to='Continent', not_found='Other')
    i += 1
burned_continents_year = (burned_countries.groupby('continent').agg({'forest': 'sum', 'savannas': 'sum',
                                                               'shrublands_grasslands': 'sum', 'croplands': 'sum',
                                                               'other': 'sum', 'total_burned_surface': 'sum'})
                     .reset_index())

burned_countries.to_csv('burned_countries.csv')
burned_countries_year.to_csv('burned_countries_year.csv')
burned_continents.to_csv('burned_continents.csv')
burned_continents_year.to_csv('burned_continents_year.csv')
