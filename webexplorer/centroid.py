import pandas as pd
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', 'header=None')
df.tail()

def ComputeShow(): 
    import matplotlib.pyplot as plt
    import numpy as np
    y = df.iloc[0:100, 4].values

    pass