import pandas as pd
from nltk import FreqDist
import numpy as np
from src.ELT.ELT import ELT
from src.ELT._analysis import absolute_ranking, prop_ranking
import matplotlib.pyplot as plt

def NAICS_word_freq():
    part1 = pd.read_csv('data/Part 1.csv', low_memory=False)
    labels_str = ''
    labels = list(set(part1['NAICS.display-label']))  # verified already to be all strings
    for item in labels:
        labels_str = item + " " + labels_str

    words = labels_str.split(" ")
    freqDist = FreqDist(words)
    freqDist.plot(10)

def estab_hist(top):
    df = ELT('stores')
    df = absolute_ranking(df.df, 'stores', top)
    df = np.asarray(df['ESTAB_stores_1000'])
    plt.hist(df, log=True)
    plt.xlabel('store establishments with revenue > $1,000,000')
    plt.ylabel('frequency')
    plt.title('Histogram of Establishment Frequencies')

def prop_hist(top1, top2):
    df = ELT('stores')
    df = absolute_ranking(df.df, 'stores', top1)
    df = prop_ranking(df, 'stores', top2)
    df = np.asarray(df['ESTAB_stores_1000'])
    plt.hist(df, log=True)
    plt.xlabel('store proportion of establishments with revenue > $1,000,000')
    plt.ylabel('frequency')
    plt.title('Histogram of Proportional Frequencies')
