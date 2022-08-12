import pandas as pd

def preprocess(df,region_df):
    #filtering the data based on summer olympics
    df = df =df[df['Season']=='Summer']
    #merge with region df
    df = df.merge(region_df, on='NOC', how='left')
    #drop duplicates
    df.drop_duplicates(inplace=True)
    #will concate based on medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df