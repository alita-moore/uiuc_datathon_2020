"""
perform analysis on the processed dataframe
"""
from src.ELT._utils import get_market

def absolute_ranking(df, market):
    """ranks area code based on absolute market performance"""
    df, labels = get_market(df, market)
    all = df[['GEO.id2', 'GEO']]