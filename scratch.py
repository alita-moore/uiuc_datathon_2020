import pandas as pd
from src.ELT.ELT import ELT
from src.ELT._utils import zip_breakdown

# load in data for markets
stores = ELT('stores')
total = ELT('total')
dealers = ELT('dealers')
other = ELT('other')

# run rannk analysis on all markets
stores.rank_analysis()
total.rank_analysis()
dealers.rank_analysis()
other.rank_analysis()

# collect the recommended zips
temp = [total, stores, dealers, other]

# merge into dataset to compare between markets
rec_zips_1000 = zip_breakdown(temp, -1)
rec_zips_500_1000 = zip_breakdown(temp, -2)



