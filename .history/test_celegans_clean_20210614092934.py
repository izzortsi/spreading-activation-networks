# %%
import graph_tool.all as gt
import numpy as np
import numpy.random as npr
# import matplotlib.colors as mplc
from matplotlib import cm
import matplotlib.colors as mplc
import os, sys
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib
from plot_functions import *



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

# %%

####DYNAMICS PARAMETERS
SPIKE_THRESHOLD = 1
POTENTIAL_LOSS = 0.8
max_count = 2000


# %%

##

# %%
count = 0

def update_state():

    global count, g

    spiker_activation = np.max(g.vp.activation.a)
    spiker = npr.choice(gt.find_vertex(g, g.vp.activation, spiker_activation), 1)[0]
    print(spiker)

    nbs = g.get_out_neighbors(spiker)
    
    nbsize = len(nbs)
    spread_val = spiker_activation/nbsize
    if nbsize != 0:
        g.vp.activation[spiker] *= POTENTIAL_LOSS
    for nb in nbs:
        g.vp.activation[nb] += spread_val
        #if g.vp.activation[nb] >= SPIKE_THRESHOLD:
             

    win.graph.regenerate_surface()
    win.graph.queue_draw()
    
    count += 1

    if count >= max_count:
        sys.exit(0)

    return True


# %%
g = set_graph()
PLOT_PARAMS = plot_params(g, None)

pos = gt.sfdp_layout(g)
win = gt.GraphWindow(g, pos, geometry=(500, 500),
    vertex_shape="circle",
    **PLOT_PARAMS
    )


# %%
npr.choice([1, 2, 3], 1)
# %%
spiker_activation = np.max(g.vp.activation.a)
spiker = npr.choice(gt.find_vertex(g, g.vp.activation, spiker_activation), 1)[0]

# %%
spiker

# %%
    
cid = GLib.idle_add(update_state)
win.connect("delete_event", Gtk.main_quit)
win.show_all()
Gtk.main()  
# %%
