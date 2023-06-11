import pandas as pd
import numpy as np
from operator import attrgetter
from IPython.display import display


def filter_table(User,df):
    filter_price,filter_location,filter_area,filter_bedrooms=1,1,1,1
    res=df
    if User.price['value'] != None:
        filter_price = df["price_VND"] <= User.price['value']
        res=res.where(filter_price)
    if User.price_lower['value'] != None:
        price_lower = df["price_VND"]/df["area_m2"] >= User.price_lower['value']
        res=res.where(price_lower)
    if User.location['value']!= None:
        filter_location =  df['location'].isin(User.location['value'])
        res=res.where(filter_location)
    if User.bedrooms['value']!= None:
        filter_bedrooms =  df["number_of_bedrooms"] >= User.bedrooms['value']
        res=res.where(filter_bedrooms)
    if User.area['value']!= None:
        filter_area = df["area_m2"] >= User.area['value']
        res=res.where(filter_area)
    #res = df.where(filter_price & filter_location & filter_area & filter_bedrooms)
    res = res.dropna()
    return res


def clean_table(df):
    df=df.drop(['Unnamed: 0'], axis=1)
    df.index.name = 'id'
    return df
def comparision(id1,id2,df):
    #pd.set_option('display.max_rows', None)
    instance1,instance2 = clean_table(df.loc[[id1]]),clean_table(df.loc[[id2]])
    frames = [instance1.T, instance2.T] 
    result = pd.concat(frames,axis=1)
    display(result)
    return result
    #pd.reset_option('display.max_rows')



if __name__ == "__main__":
    df = pd.read_csv('cleaned.csv')
    df = df.dropna()
    display(df.head())