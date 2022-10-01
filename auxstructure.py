from lib import *

def auxstructure(elem):
    totalEdge = np.sort(np.concatenate((elem[:,[1,2]],elem[:,[2,0]],elem[:,[0,1]]),axis=0))
    edge,i2,j = np.unique(totalEdge,return_index=True,return_inverse=True)
    return totalEdge,edge,i2,j
    