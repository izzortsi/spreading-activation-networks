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

"""
TODO
The sinks (non-isolated vertices without out-neighbors) must do something.
I'd like to put them to reproduce, as if they were "accumulating" too much
activation and needed to dissipate it, without any means to do so
"""

def init_graph():
    g = gt.collection.data["celegansneural"]
    treemap = gt.min_spanning_tree(g)
    gmst = gt.GraphView(g, efilt=treemap)
    gmst = gt.Graph(gmst, prune=True)
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
    print(g)
    g.ep.weight.a = eweights

    return g


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

    g = set_graph_properties(g)

    return g



# %%

# %%

####DYNAMICS PARAMETERS
SPIKE_THRESHOLD = 0.90
POTENTIAL_LOSS = 0.8
MAX_COUNT = 600
#OFFSCREEN = True
OFFSCREEN = sys.argv[1] == "offscreen" if len(sys.argv) > 1 else False

# %%

##

# %%
count = 0

def update_state():

    global count, g

    spiker_activation = np.max(g.vp.activation.a)

    spiker = gt.find_vertex(g, g.vp.activation, spiker_activation)[0]

    nbs = g.get_out_neighbors(spiker)
    
    nbsize = len(nbs)
    
    if nbsize != 0:
        spread_val = spiker_activation/nbsize
        for nb in nbs:
            g.vp.activation[nb] += spread_val
    
    g.vp.activation[spiker] *= POTENTIAL_LOSS
    
        #if g.vp.activation[nb] >= SPIKE_THRESHOLD:
             

    win.graph.regenerate_surface()
    win.graph.queue_draw()
        
    if OFFSCREEN:
        pixbuf = win.get_pixbuf()
        pixbuf.savev(r'./frames/san%06d.png' % count, 'png', [], [])
    
    count += 1

    if count >= MAX_COUNT:
        sys.exit(0)

    return True


# %%
g = set_graph(type="gtc")
pos = gt.sfdp_layout(g)
PLOT_PARAMS = plot_params(g, None)


if OFFSCREEN and not os.path.exists("./frames"):
    os.mkdir("./frames")

# This creates a GTK+ window with the initial graph layout
if not OFFSCREEN:
    win = gt.GraphWindow(g, 
    pos, 
    geometry=(720, 720),
    vertex_shape="circle",
    **PLOT_PARAMS,
    )
else:
    win = Gtk.OffscreenWindow()
    win.set_default_size(720, 720)
    win.graph = gt.GraphWidget(g, 
    pos,
    vertex_shape="circle",
    **PLOT_PARAMS,
    )
    win.add(win.graph)


# %%
    
cid = GLib.idle_add(update_state)
win.connect("delete_event", Gtk.main_quit)
win.show_all()
Gtk.main()  
# %%

# %%
