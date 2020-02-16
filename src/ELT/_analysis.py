"""
perform analysis on the processed dataframe
"""
import pandas as pd
from src.ELT._utils import get_market, getprop

def absolute_ranking(df, market, top):
    """ranks area code based on absolute market performance"""
    df, labels = get_market(df, market)

    # collect only the highest absolute values for each column
    temp = [df[[labels[0], labels[i]]].dropna().sort_values(by=[labels[i]]).tail(top) for i in range(2, 8)]

    # combine/simplify
    df = df[[labels[0], labels[1]]].drop_duplicates(subset=labels[0])
    for i in range(6):
        df = df.merge(temp[i], on=labels[0], how='left')
    df = df.dropna(thresh=3)

    return df

def prop_ranking(df, market, top):
    df, labels = get_market(df, market)
    df = getprop(df, labels)

    temp = []
    for i in range(3, 8):
        temp.append(df[[labels[0], labels[i]]].dropna().sort_values(by=[labels[i]]).tail(top))

    df = df[[labels[0], labels[2]]].drop_duplicates(subset=labels[0])
    for i in range(5):
        df = df.merge(temp[i], on=labels[0], how='left')
    df = df.dropna(thresh=3)

    return df






