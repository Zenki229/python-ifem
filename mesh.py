from lib import *

# Content
# SquareMesh: generate mesh for a square
# ShowMesh: plot 2D mesh
# AuxStructure: generate auxiliary structure for a 2D mesh
# Copyright (C) Long Chen.


# This is the part of generate mesh
class SquareMesh:
    # generate square mesh with (Mx+1)*(My+1) points of square including boundary
    # Here I recommend to divide interval (x0,x1) into M+1 pieces, h = 1/M
    def __init__(self, square, Mx, My):
        x0, x1, y0, y1 = square
        [x_grid, y_grid] = np.meshgrid(np.linspace(x0, x1, num=Mx + 1), np.linspace(y0, y1, num=My + 1))
        self.node = np.concatenate((x_grid.reshape(-1, 1), y_grid.reshape(-1, 1)), axis=1)
        num_row, num_col = x_grid.shape
        num_node = self.node.shape[0]
        tri2node = np.arange(num_node - num_col)
        top_node = np.arange(start=num_col - 1, stop=num_node - num_col, step=num_col)
        tri2node = np.delete(tri2node, top_node)
        k = tri2node.transpose()
        self.elem = np.concatenate((np.stack((k + num_col, k + num_col + 1, k), axis=1), np.stack((k + 1, k, k + num_col + 1), axis=1)), axis=0)


class CircleMesh:
    # Generate CircMesh with uniform distance
    pass

# This is the part of draw mesh


class ShowMesh:
    # Set the param pair('FaceAlpha',value) to change transparency
    # 'FaceColor','EdgeColor'
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


class FindBoundary:
    # find Dirichlet boundary nodes and Neumann edges. The boundary edges  found using bd_flag is counterclockwise
    def __init__(self, elem, bd_flag):
        nn = np.max(elem.flatten())
        num_dim = elem.shape[1]
        if num_dim == 3:  # triangle
            total_edge = np.concatenate((elem[:, [1, 2]], elem[:, [2, 0]], elem[:, [0, 1]]), axis=0)
        elif num_dim == 4:  # quad
            total_edge = np.concatenate((elem[:, [1, 2]], elem[:, [2, 3]], elem[:, [3, 0]], elem[:, [0, 1]]), axis=0)






