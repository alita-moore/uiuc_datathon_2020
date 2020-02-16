"""
main ELT script that loads, processes, and manages packages

# TODO: turn into a class to increase robust
"""
import os
import pandas as pd
from src.ELT._utils import init_params
from src.ELT._process import process_raw, process_analysis, combine

class ELT:
    def __init__(self, market, **kwargs):
        """
        :param market: the purpose of this class is to organize market analysis; ['stores', 'dealers', 'other', 'total']
        :param kwargs:
        'parts', the part data files you want to process for this analysis
        'force_process', force process part files? use if _process.py has been updated
        """
        # preamble
        params = {'parts': ['Part 1', 'Part 2', 'Part 3', 'Part 4a', 'Part 4b', 'Part 5'], 'force_process': False}
        params = init_params(params, kwargs)
        parts, force_process = params['parts'], params['force_process']

        # check data_dir exists
        if not os.path.exists('data'):
            raise OSError("'./data directory was not found; provided the scope of this project, this relative path"
                          "is required. i.e. /data/Part 1.csv is a required recognized path")

        # establish object
        self.df = pd.DataFrame()
        self.load(parts, force_process)  # the main object of this method that updates as you do things
        self.market = market

        # other items
        self.base = pd.DataFrame(self.df['GEO.id2'].drop_duplicates())  # for external use

    def load(self, parts, force_process):
        """load/process all desired parts"""
        for part in parts:
            if force_process:
                process_raw(part)  # saves to appropriate location
            elif not os.path.exists('data/' + part + '_processed.p'):
                process_raw(part)

        self.df = combine(parts)  # runs everytime; though unoptimal, it simplifies code and is fast anyway

    def rank_analysis(self, **kwargs):
        """performs ranking analysis and saves output
        'absolute_top' and 'proportional_top' are accepted arguments"""
        # preamble
        params = {'absolute_top': 2000, 'proportional_top': 10}
        params = init_params(params, kwargs)
        absolute_top, proportional_top = params['absolute_top'], params['proportional_top']

        self.df = process_analysis(self.df, absolute_top, proportional_top, self.market)

    def rec_zip(self):
        """output/recommend top zips based on the category"""
        labels = ['GEO.id2', 'ESTAB_' + self.market + '_all', 'ESTAB_' + self.market + '_entire_year',
               'ESTAB_' + self.market + '_0_100', 'ESTAB_' + self.market + '_100_250', 'ESTAB_' + self.market + '_250_500',
               'ESTAB_' + self.market + '_500_1000', 'ESTAB_' + self.market + '_1000']
        temp = []
        for i in range(3, 8):
            temp.append(self.df[[labels[0], labels[2], labels[i]]].dropna())

        return temp
