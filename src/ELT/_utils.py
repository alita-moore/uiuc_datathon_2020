"""
collection of utility functions
"""
import pandas as pd


def get_market(df, market):
    """returns the market only df values"""
    columns = ['GEO.id2', 'ESTAB_' + market + '_all', 'ESTAB_' + market + '_entire_year',
               'ESTAB_' + market + '_0_100', 'ESTAB_' + market + '_100_250', 'ESTAB_' + market + '_250_500',
               'ESTAB_' + market + '_500_1000', 'ESTAB_' + market + '_1000']
    return df[columns], columns


def get_tot_estab(df, unique):
    """df is assumed to be prior sorted for values of interest
    returns sorted list with zip as key"""
    temp = df[['GEO.id2', 'ESTAB']]
    name = 'ESTAB_' + unique  # unique is to establish new column name
    temp = temp.groupby(['GEO.id2']).sum().reset_index()
    temp = temp.rename(columns={'ESTAB': name}).sort_values(by=name)
    return temp


def estab_breakdown(df, market, srch):
    """calculates the number of establishments per
    tax segment and based on defined market"""
    base = pd.DataFrame(df['GEO.id2'].drop_duplicates())
    labels = ['all', 'entire_year', '0_100', '100_250', '250_500', '500_1000', '1000']
    for i, label in enumerate(labels):
        label = market + '_' + label
        temp = get_tot_estab(df.loc[df['RCPSZFE.id'] == srch[i]], label)
        base = base.merge(temp, on='GEO.id2', how='left')
    return base


def getdf(input, columns):
    """takes a list of lists and turns into a df"""
    if len(input) != len(columns):
        raise("the dimensions are off for your input, this should be a list of lists with corresponding"
              "desired column names; i.e. [[1,2],['a','b']], ['num', 'letter']")

    temp = {}
    for i, item in enumerate(columns):
        temp[item] = input[i]

    return pd.DataFrame.from_dict(temp)


def getprop(df, labels):
    """transform: proportional value; index [3:] by 2nd index in labels
    requires consistent labeling to get_market()"""
    for i in range(3, 8):
        temp = df[[labels[2], labels[i]]].dropna()
        df[labels[i]] = temp[labels[i]] / temp[labels[2]]
    return df


def init_params(params, kwargs):
    """ assign optional parameters to actual values"""
    for item in kwargs:
        if item in params:
            params[item] = kwargs[item]
    return params

def zip_breakdown(temp, cat):
    """simplification for getting the combined
    market performance for a given finacial category
    :param list[DataFrame] temp: returned dfs from ELT.rank_analysis()
    :param int cat: desired category index in ELT.rec_zip() -> list[DataFrame]
    """
    df = temp[0].base  # same for all markets
    for i in temp:
        j = i.rec_zip()
        j[cat]['ESTAB_' + i.market + '_1000'] = j[cat].apply(lambda row: int(row[1] * row[2]), axis=1)
        j[cat] = j[cat].drop(columns=['ESTAB_' + i.market + '_entire_year'])
        df = df.merge(j[cat], on='GEO.id2', how='left')
    df = df.dropna(thresh=2)  # drop zips not recommended
    return df
