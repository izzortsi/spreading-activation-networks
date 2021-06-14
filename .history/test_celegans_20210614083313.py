# %%
import graph_tool.all as gt
import numpy as np
import numpy.random as npr
# import matplotlib.colors as mplc
from matplotlib import cm
import matplotlib.colors as mplc
import os, sys
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib


# %%
GRAD_FACTOR = 50
# %%

def make_gradient():
    #grad = np.linspace(0, 1, 20, endpoint=True)
    grad = (np.logspace(0, 1, GRAD_FACTOR, endpoint=True) -1)/9
    colors = [(c, c, c) for c in grad]
    cmap = mplc.LinearSegmentedColormap.from_list("gscale", colors, N=GRAD_FACTOR)
    return cmap

def plot_params(g, cmap):
    if cmap is None:
        CMAP = make_gradient()
    else:
        CMAP = cmap    
    PLOT_PARAMS = {"K": 1.0, "vertex_size": 6}
    PLOT_PARAMS["vertex_fill_color"] = g.vp.activation
    PLOT_PARAMS["vertex_color"] = "black"
    PLOT_PARAMS["vcmap"] = CMAP
    PLOT_PARAMS["edge_fill_color"] = g.ep.weight
    PLOT_PARAMS["ecmap"] = CMAP

    return PLOT_PARAMS

def plot_graphs(graph_list, cmap=None):
    
    if type(graph_list) == list:
        for graph in graph_list:    
            ppms = plot_params(graph, cmap)   
            gt.graph_draw(graph, output_size=(450, 450), **ppms)
    
    else:
        graph = graph_list 
        ppms = plot_params(graph, cmap) 
        gt.graph_draw(graph, output_size=(450, 450), **ppms)


def plot_gtk(g):

    PLOT_PARAMS = plot_params(g, None)

    pos = gt.sfdp_layout(g)
    win = gt.GraphWindow(g, pos, geometry=(500, 500),
    vertex_shape="circle",
    **PLOT_PARAMS
    )
    win.connect("delete_event", Gtk.main_quit)
    win.show_all()
    Gtk.main()        


# %%


def init_graph():
    g = gt.collection.data["celegansneural"]
    treemap = gt.min_spanning_tree(g)
    gmst = gt.GraphView(g, efilt=treemap)
    gtclos = gt.transitive_closure(gmst)
    
    return {"g": g, "gmst": gmst, "gtc": gtclos}


def minmax(a):
    a = (a - np.min(a))
    return a/np.max(a)


def set_graph_properties(g):
    
    g.vp.state = g.new_vertex_property("int")
    g.vp.activation = g.new_vertex_property("float")
    g.ep.weight = g.new_edge_property("float")

    n_vertices = g.num_vertices()
    n_edges = g.num_edges()

    activations = npr.normal(size=n_vertices)
    activations = minmax(activations)
    
    eweights = npr.normal(size=n_edges)
    eweights = minmax(eweights)
    
    print(f"activations: max {np.max(activations)}, min {np.min(activations)}")
    print(f"eweights: max {np.max(eweights)}, min {np.min(eweights)}")
    # print(activations)
    g.vp.state.a = np.full(n_vertices, 0)
    g.vp.activation.a = activations
    g.ep.weight.a = eweights


# %%
"""
def set_graph(type="gtc")

type being either the original graph "g", the MST of it
"gmst" or the transitive closure of the MST "gtc". Defaults
to "gtc".
"""
def set_graph(type="gtc"):

    graphs = init_graph()

    g = graphs[type]

    set_graph_properties(g)

    return g



# %%
g = set_graph()
plot_graphs(g)
# %%

####AGORA COMEçA A DINAMICA

def update_state():
    pass

if __name__ == "__main__":
    g = set_graph()
    plot_gtk(g)