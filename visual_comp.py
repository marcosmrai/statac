# -*- coding: utf-8 -*-
import sys
import os 
import numpy as np

__FILE_NAME = os.path.basename(__file__)
__FILE_FOLDER = os.path.abspath(__file__).replace(__FILE_NAME, "")

sys.path+=[__FILE_FOLDER]

import nonparametric_tests as non
import igraph

def multitest(threat, names, threshold=0.01, multi_test='skillings_test', multi_posthoc='finner_multitest', imgpath=None, subset=None):
    func_test = getattr(non, multi_test)
    func_posthoc = getattr(non, multi_posthoc)
    
    if subset==None:
        subset=names
    
    Fvalue, pvalue, ranking, pivots = func_test(*threat)
    
    multiargs = {nam:ran for nam,ran in zip(names, pivots)}
    
    if pvalue<threshold:
        comps,_,_,pns = func_posthoc(multiargs)
        
        g = igraph.Graph(directed=True)
        g.add_vertices(len(subset))
        g.vs["name"] = subset
        g.vs["label_dist"] = -3
        g.vs["label"] = g.vs["name"]
        g.vs["color"] = 'white'
        g.vs["label_size"] = 25
        g.layout_circle()
        
        for comp,pn in zip(comps,pns):
            n1,n2 = comp.split(' vs ')
            if not n1 in subset:
                continue
            if not n2 in subset:
                continue
            i1 = subset.index(n1)
            i2 = subset.index(n2)
            if pn<threshold:
                if pivots[i1]<pivots[i2]:
                    g.add_edges([(i1,i2)])
                else:
                    g.add_edges([(i2,i1)])
        layout = g.layout_circle()
        if imgpath==None:
            igraph.plot(g, layout = layout, margin = 40)
        else:
            igraph.plot(g, imgpath, layout = layout, margin = 40)

        return np.array(g.get_adjacency().data)
    else:
        return None
