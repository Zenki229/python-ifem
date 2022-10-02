from lib import *


#def auxstructure(elem):
  #  totalEdge = np.sort(np.concatenate((elem[:,[1,2]],elem[:,[2,0]],elem[:,[0,1]]),axis=0))
   # edge,index_last,inv_index = np.unique(totalEdge,return_index=True,return_inverse=True,axis=0)
   # return totalEdge,edge,index_last,inv_index

class AuxStructure():
    def __init__(self,elem):
        totalEdge = np.sort(np.concatenate((elem[:,[1,2]],elem[:,[2,0]],elem[:,[0,1]]),axis=0))
        self.edge, index_last, inv_index = np.unique(totalEdge, return_index=True, return_inverse=True, axis=0)
        NT = elem.shape[0]
        self.Elem2Edge = inv_index.reshape(NT,3,order='F')
        index_first = np.empty_like(index_last)
        index_first[inv_index] = np.arange(3*NT)
        local_location_first = np.floor(index_first/NT).astype('int32')
        local_location_last = np.floor(index_last/NT).astype('int32')
        global_location_first = index_first-NT*(local_location_first)
        global_location_last = index_last-NT*(local_location_last)
        index_inter = np.not_equal(index_first,index_last)
        self.Edge2Elem = np.concatenate((global_location_first,global_location_last,\
                                         local_location_first,local_location_last)).reshape((-1,4),order='F')
        ind1 =np.concatenate((global_location_first[index_inter],local_location_first[index_inter]))\
                            .reshape((-1,2),order='F')
        ind2 =np.concatenate((global_location_last,local_location_last)).reshape((-1,2),order='F')
        weights=np.concatenate((global_location_last[index_inter],global_location_first))
        self.neighbor = accum(np.concatenate((ind1,ind2),axis=0),weights).reshape((NT,3),order='F')
        self.BdElem = 1






