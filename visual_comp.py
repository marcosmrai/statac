# -*- coding: utf-8 -*-
import sys
import os 
import numpy as np

__FILE_NAME = os.path.basename(__file__)
__FILE_FOLDER = os.path.abspath(__file__).replace(__FILE_NAME, "")

sys.path+=[__FILE_FOLDER]

import nonparametric_tests as non
import igraph

def multitest(threat, names, threshold=0.01, multi_test='skillings_test', multi_posthoc='finner_multitest', plot=None, subset=None):
    func_test = getattr(non, multi_test)
    func_posthoc = getattr(non, multi_posthoc)
    
    if subset==None:
        subset=names
    
    Fvalue, pvalue, ranking, pivots = func_test(*threat)
    
    multiargs = {nam:ran for nam,ran in zip(names, pivots)}
    
    if pvalue<threshold:
        A = np.zeros((len(names),len(names)))
        comps,_,_,pns = func_posthoc(multiargs)
        
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
                    #print(n1+' is better than '+n2)
                    A[i1,i2] = 1
                else:
                    #print(n2+' is better than '+n1)
                    A[i2,i1] = 1
        
        if plot!=False:
            g = igraph.Graph(directed=True).Adjacency(A.tolist())
            g.vs["name"] = subset
            g.vs["label_dist"] = -3
            g.vs["label"] = g.vs["name"]
            g.vs["color"] = 'white'
            g.vs["label_size"] = 25
            layout = g.layout_circle()
            if plot==True:
                igraph.plot(g, layout = layout, margin = 40)
            else:
                igraph.plot(g, plot, layout = layout, margin = 40)            

        return A, ranking
    else:
        return None
