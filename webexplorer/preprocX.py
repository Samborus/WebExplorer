import pandas as pd
from io import StringIO
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import csv

class PreProcX:
    def __init__(self): 
        self.csv_data = 'ref003.csv'
        self.data = np.array([0,0,0,0,0,0,0,0,0,0])

    def preGo(self):        

        # eżeli korzystasz ze środowiska Python 2.7, musisz
        # przekonwertować ciąg znaków do standardu unicode:
        # csv_data = unicode(csv_data)
        from numpy import genfromtxt
        my_data = np.genfromtxt(self.csv_data, delimiter=';')

        self.data = np.array(None)
        with open(self.csv_data, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            i = 0
            for row in reader:
            #df = pd.read_csv(StringIO(self.csv_data))
                #if i > 0:
                np.append(self.data, row)
                i += 1
            pass
        X_train = np.ravel(row)
        mms = MinMaxScaler()
        X_train_norm = mms.fit_transform(X_train)

        stdsc = StandardScaler()
        X_train_std = stdsc.fit_transform(X_train)
        pass