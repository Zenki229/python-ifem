from lib import *

# Content:
# BoundEdges: find boundary edges from trianngular mesh
# Copyright (C) 2004-2006 Per-Olof Persson. See COPYRIGHT.TXT for details.


class BoundEdges:
    def __init__(self, node, elem):
        edge = np.sort(np.concatenate((elem[:, [1, 2]], elem[:, [2, 0]], elem[:, [0, 1]]), axis=0))