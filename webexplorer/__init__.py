from core import *
# from centroid import *

if __name__ == "__main__":    
    # ComputeShow()
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
    

