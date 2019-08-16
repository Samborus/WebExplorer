from core import *
# from centroid import *
#from Percep01 import *
from PUM1 import *
from PUM2 import *
import matplotlib.pyplot as plt
import numpy as np
from sigmoid import *
from rand1 import *
from preprocX import *

if __name__ == "__main__":  
    pre = PreProcX()
    #pre.preGo()
    
    if not True:  
        vievwer1()
    
    sig = sigmod()
    #sig.show()
    work = Worker()
    #work.do()
    #do2()
    # No2
    
    #perceptron = Perceptron()
    #perceptron.fit(10, 10)
    #omputeShow()
    if True:
        appContext = AppContext('config.cfg')
        appContext.GetConfiguration()
        print('URL = ' + appContext.data['Url'])
        for x in range(1):
            timePoint = datetime.datetime.now()
            print('------------------------------------')
            print('Loop | Start | ' + str(x))                
            program = WebExplorer(appContext, True)
            program.Go()
            timePoint = datetime.datetime.now() - timePoint
            ite = program.links.__len__()
            for x in range(ite):

                pass
            print('Loop | End | ' + str(timePoint))
            print(*program.links, sep = '\n')
    

