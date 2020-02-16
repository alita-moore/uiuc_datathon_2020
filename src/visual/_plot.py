import pandas as pd
from nltk import FreqDist
import numpy as np
import matplotlib.pyplot as plt

def NAICS_word_freq():
    part1 = pd.read_csv('data/Part 1.csv', low_memory=False)
    labels_str = ''
    labels = list(set(part1['NAICS.display-label']))  # verified already to be all strings
    for item in labels:
        labels_str = item + " " + labels_str

    words = labels_str.split(" ")
    freqDist = FreqDist(words)
    freqDist.plot(20)
