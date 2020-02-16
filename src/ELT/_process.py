"""
Processes the raw data into important information so that it's more manageable for later analysis;
these functions have the common trope of taking in a df and outputting a cleaned version
** requires data to be in '/data/...' from the main directory

methods:
process_raw: brings down the raw size from ~175MB to ~3MB; total down to ~16MB
combine: combines desired processed parts into a single df; remembers which part each datapoint is from
process_analysis: runs absolute and proportional ranking in tandum; produces focused df
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.ELT._utils import estab_breakdown
from src.ELT._analysis import absolute_ranking, prop_ranking

def process_raw(part):
    """
    extract important information
    :param str part: the raw csv to process
    :return: prints plt histogram
    """
    try:
        df = pd.read_csv('data/' + part + '.csv', low_memory=False)
    except OSError:
        raise OSError('please input a valid part id...')

    # preamble
    df = df.iloc[1:, :]  # removes description
    df['ESTAB'] = df['ESTAB'].astype(int)  # for later establishment calculations

    # Debug/remove error
    if part in ['Part 4a', 'Part 4b']:
        srch = ['1', '2', '114', '123', '125', '131', '132', '998']  # debug
        temp = df.loc[df['RCPSZFE.id'] == '1']
    else:
        srch = ['001', '002', '114', '123', '125', '131', '132', '998']
        temp = df.loc[df['RCPSZFE.id'] == '001']
    df = df.loc[df['GEO.id2'].str.len() == 5]

    # frequency of zip codes
    zip_occur = temp.groupby(by='GEO.id2').size().reset_index().rename(columns={0: 'zip_count'}).sort_values(
        by='zip_count')  # unnecessary because len(NAICS_id) is equivalent; left in for simplicity later

    # stores all data for later use if necessary -- POTENTIAL FOR DEPRECATION
    NAICS_id = pd.DataFrame(
        temp.groupby('GEO.id2').apply(lambda x: x['NAICS.display-label'].unique()).reset_index().rename(columns={0: 'NAICS_ids'}))  # np array of NAICS ids associated with zip
    NAICS_estab = pd.DataFrame(
        temp.groupby('GEO.id2').apply(lambda x: np.asarray(x['ESTAB'])[np.unique(x['NAICS.display-label'], return_index=True)[1]]).reset_index().rename(columns={0: 'NAICS_estab'}))

    # market segmentation
    estab_all = estab_breakdown(df, 'total', srch)
    estab_stores = df.loc[df['NAICS.display-label'].str.contains('stores', case=False)]
    estab_stores = estab_breakdown(estab_stores, 'stores', srch)
    estab_dealers = df.loc[df['NAICS.display-label'].str.contains('dealers', case=False)]
    estab_dealers = estab_breakdown(estab_dealers, 'dealers', srch)
    estab_other = df.loc[~(df['NAICS.display-label'].str.contains('|'.join(['stores', 'dealers'])))]
    estab_other = estab_breakdown(estab_other, 'other', srch)

    # recombine into final df
    df = df['GEO.id2'].drop_duplicates().reset_index().drop(columns=['index'])
    df = df.merge(zip_occur, on='GEO.id2', how='left')  # TODO: simplify this implementation in for loop (for whole method)
    del zip_occur  # optimizations ...
    df = df.merge(estab_all, on='GEO.id2', how='left')
    del estab_all
    df = df.merge(estab_stores, on='GEO.id2', how='left')
    del estab_stores
    df = df.merge(estab_dealers, on='GEO.id2', how='left')
    del estab_dealers
    df = df.merge(estab_other, on='GEO.id2', how='left')
    del estab_other
    df = df.merge(NAICS_id, on='GEO.id2', how='left')
    del NAICS_id
    df = df.merge(NAICS_estab, on='GEO.id2', how='left')

    # save results
    df.to_pickle('data/' + part + '_processed.p')

    return df

def combine(parts):
    """
    combine the processed pickles
    :param list[str] parts: the parts to combine
    :return: combined df
    """
    temp = []
    for part in parts:
        df = pd.read_pickle('data/' + part + '_processed.p')
        df['part'] = part  # for later reference
        temp.append(df)
    temp = pd.concat(temp)
    temp.to_pickle('data/combined_' + str(len(parts)) + '_parts.p')
    return temp

def process_analysis(df, top1, top2, market):
    """
    perform analysis processing
    :param DataFrame df: processed data
    :param int top1: absolute top values (used for ensuring enough data in sample; e.g. 'stores' top1 = 2000)
    :param int top2: proportional top values (as in top 10 per category)
    :param str market: the market to analyze (e.g. 'stores') note that the implementation here is not dynamic
    :return DataFrame:
    """
    df = absolute_ranking(df, market, top1)
    df = prop_ranking(df, market, top2)
    df.to_pickle("data/analysis_" + market + ".p")

    return df

