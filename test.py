import streamlit as st
import pandas as pd
import preprocessor,helper


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
#filtering the data based on summer olympics
df = df[df['Season']=='Summer']
#merge with region df
df = df.merge(region_df, on='NOC', how='left')
#drop duplicates
df.drop_duplicates(inplace=True)
#will concate based on medals
df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0

    if year == 'overall' and country == 'overall':
        temp_df = medal_df

    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if year != 'overall' and country == 'overall':
        temp_df = medal_df[medal_df['Year'] == year]

    if year != 'overall' and country != 'overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == year)]

    x = temp_df

    if flag == 1:
        x = x.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                          ascending=True).reset_index()

    else:
        x = x.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                            ascending=False).reset_index()

        x['total'] = x['Gold'] + x['Silver'] + x['Silver']
    return x


fetch_medal_tally(df,2016,'overall')