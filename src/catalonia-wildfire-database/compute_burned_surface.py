#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import geopandas as gpd

burned_area_by_years = {'year': list(), 'surface': list()}
for i in range(1986, 2023):
    gdf = gpd.read_file('./incendis-catalunya-1986-2022.gpkg', layer='incendis{0:}'.format(i))
    burned_area_by_years['year'].append(i)
    burned_area_by_years['surface'].append(gdf.area.sum())
burned_area_year_gis = pd.DataFrame(data=burned_area_by_years)
burned_area_year_gis.to_csv('burned_area_by_years_gis.csv')

burned_area_by_years = {'year': list(), 'surface': list()}
burned_area = pd.read_csv('./Incendis_forestals_a_Catalunya._Anys_2011-2022.csv')
burned_area['date'] = pd.to_datetime(burned_area['DATA INCENDI'], format='%d/%m/%Y')
burned_area['year'] = burned_area['date'].dt.year
burned_area_year_opendata = burned_area.groupby('year').agg({'HANOFOREST': 'sum', 'HAFORESTAL': 'sum'})
burned_area_year_opendata['total'] = burned_area_year_opendata['HANOFOREST'] + burned_area_year_opendata['HAFORESTAL']
burned_area_year_opendata.to_csv('burned_area_by_years_opendata.csv')
