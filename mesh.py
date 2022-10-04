from lib import *

# Copyright (C) Long Chen.
######################### This is the part of generate mesh #################################################3#
class SquareMesh():
    # generate squaremesh with uniform distance and given nodes [x0,x1,y0,y1]
    # Here I recommend to divide interval (x0,x1) into M+1 pieces, h = 1/M
    def __init__(self,square,Mx,My):
        x0,x1,y0,y1=square
        # I prefer ndgrid in Matlab, so I use ndgrid here
        [X,Y]=np.meshgrid(np.linspace(x0,x1,num=Mx+1),np.linspace(y0,y1,num=My+1))
        self.Node = np.concatenate((X.reshape(-1,1),Y.reshape(-1,1)),axis = 1)
        Num_Row =X.shape[0]
        Num_Node=self.Node.shape[0]
        Tri2Node_Index_Map=np.arange(Num_Node-Num_Row)
        TopNode= np.arange(Num_Row-1,Num_Node-Num_Row,Num_Row)
        Tri2Node_Index_Map = np.delete(Tri2Node_Index_Map,TopNode)
        k = Tri2Node_Index_Map.transpose()
        self.Elem=np.concatenate((np.stack((k+Num_Row,k+Num_Row+1,k),axis=1),np.stack((k+1,k,k+Num_Row+1),axis=1)),axis=0)

class CircleMesh():
    # Generate CircMesh with uniform distance
    pass

#################### This is the part of draw mesh########################################

class ShowMesh():
    #Set the param pair('FaceAlpha',value) to change transparency
    #'FaceColor','EdgeColor'
    def __init__(self,Node,Elem,*args):
        Dim_Node = Node.shape[1]
        Dim_Elem=Elem.shape[1]
        if (Dim_Node==2) and (Dim_Elem==3): #Planar triangulation
            Fig=plt.triplot(Node[:,0],Node[:,1],Elem)
            #Fig.set_facecolor((0.5,0.9,0.45))
        plt.show()





################### This is the part of generate auxfunction of mesh########################################
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
        index_Bound = np.equal(global_location_first,global_location_last)
        self.BdElem =global_location_first[index_Bound]
        Bd_local_index_first = local_location_first[index_Bound]
        self.BdEdge=np.concatenate((elem[np.ix_(self.BdElem[Bd_local_index_first == 0],[1,2])],\
                                    elem[np.ix_(self.BdElem[Bd_local_index_first == 1],[2,0])],\
                                    elem[np.ix_(self.BdElem[Bd_local_index_first == 2],[0,1])]),axis = 0)
        self.BdEdge2Elem = np.concatenate((self.BdElem[Bd_local_index_first ==0],self.BdElem[Bd_local_index_first == 1],\
                                           self.BdElem[Bd_local_index_first == 2]),axis = 0)







