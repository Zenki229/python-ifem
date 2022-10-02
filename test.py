from lib import *
from mesh import *

elem = np.array([[4,5,1],[5,6,2],[7,8,4],[8,9,5],[2,1,5],[3,2,6],[5,4,8],[6,5,9]])
#print(elem[:,[1,2]])#
T = AuxStructure(elem)
print(T.neighbor)
