import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.ELT._process import process_raw, combine
from src.ELT._utils import getdf

# df = pd.read_csv('data/Part 1.csv', low_memory=False).iloc[1:]
# df = df.iloc[1:, :]  # removes description
# df['ESTAB'] = df['ESTAB'].astype(int)  # for later establishment calculations
# temp = df.loc[df['RCPSZFE.id'] == '001']  # count unique institutes in region

parts = ['Part 1', 'Part 2', 'Part 3', 'Part 4a', 'Part 4b', 'Part 5']
for part in parts:
    result = process_raw(part)
test = process_raw('Part 4a')
df = combine(parts).reset_index().drop(columns='index')
# i = 0
#
# def func(labels, estab, _cats, index):
#     """counts total, returns new column values"""
#     print(index)
#     _df = getdf([labels, estab], ['labels', 'estabs'])
#     result = []
#     for cat in _cats:
#         result.append(sum(_df.loc[_df['labels'].str.contains(cat, case=False)]['estabs']))  # category sum
#     result.append(sum(_df.loc[~(_df['labels'].str.contains('|'.join(_cats)))]['estabs']))  # other sum
#     return result  # 1xn+1 : len(n) = len(_cats)


# cats = ['stores', 'dealers']  # distinguishing labels found via freq analysis
# temp = pd.DataFrame()
# temp['breakdown'] = df.apply(lambda row: func(row['NAICS_ids'], row['NAICS_estab'], cats, row.name), axis=1)
# temp = [[j[i] for j in temp['breakdown'].to_list()] for i in range(len(cats) + 1)]


# test = result[['NAICS_ids', 'NAICS_estab']].iloc[0]
# cats = ['stores', 'dealers']
# labels = test[0]
# estabs = test[1]
# _df = getdf([labels, estabs], ['labels', 'estabs'])

####
# finding word frequency
# part1 = pd.read_csv('data/Part 1.csv', low_memory=False)
# labels_str = ''
# test = part1[['NAICS.id', 'NAICS.display-label']]
# test = test.drop_duplicates(subset=['NAICS.id'])
