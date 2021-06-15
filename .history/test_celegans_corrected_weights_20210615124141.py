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

def init_elegans_net():
    
    g = gt.collection.data["celegansneural"]
    
    g.ep.weights = g.new_ep("double")
    norm_eweights = minmax(g.ep.value.a)
    g.ep.weights.a = norm_eweights

    del g.ep["value"]
    del g.gp["description"]
    del g.gp["readme"]
    del g.vp["label"]
    
    g.vp.state = g.new_vertex_property("int")
    g.vp.activation = g.new_vertex_property("float")
        
    n_vertices = g.num_vertices()
    n_edges = g.num_edges()

    activations = npr.normal(size=n_vertices)
    activations = minmax(activations)

    g.vp.state.a = np.full(n_vertices, 0)
    g.vp.activation.a = activations

    return g

# %%

def init_graph(g):

    treemap = gt.min_spanning_tree(g)
    gmst = gt.GraphView(g, efilt=treemap)
    gtclos = gt.transitive_closure(gmst)
    
    return {"g": g, "gmst": gmst, "gtc": gtclos}


def minmax(a):
    a = (a - np.min(a))
    return a/np.max(a)



# %%
"""
def set_graph(type="gtc")

type being either the original graph "g", the MST of it
"gmst" or the transitive closure of the MST "gtc". Defaults
to "gtc".
"""
def set_graph(type="gtc"):
    g = init_elegans_net()
    graphs = init_graph(g)
    g = graphs["g"]
    gmst = graphs["gmst"]
    gtc = graphs["gtc"]

    return g, gmst, gtc



# %%

# %%

####DYNAMICS PARAMETERS
SPIKE_THRESHOLD = 0.90
POTENTIAL_LOSS = 0.8
MAX_COUNT = 600
#OFFSCREEN = True
OFFSCREEN = sys.argv[1] == "offscreen" if len(sys.argv) > 1 else False

# %%
g, gmst, gtc = set_graph()

g = gmst



# %%
nbs1 = g.get_all_neighbors(g.get_all_neighbors(1))

# %%
nbs1 = set(nbs1)

# %%
nbs1
# %%
nbs2 = g.get_all_neighbors(g.get_all_neighbors(2))

# %%

nbs2
# %%
g.get_out_degrees(nbs2)
# %%
nbs2 = set(nbs2)


# %%
len(nbs1.intersection(nbs2))


# %%
a = npr.randint(100, size=100)

# %%
a
# %%
chosen = npr.choice(g.get_vertices())

# %%
print(chosen)
# %%
set(a)
# %%
while not chosen in set(a):
    chosen = npr.choice(g.get_vertices())
print(chosen)

# %%

count = 0

# %%

def update_state():

    global count, g

    spiker_activation = np.max(g.vp.activation.a)

    spiker = gt.find_vertex(g, g.vp.activation, spiker_activation)[0]

    nbs = g.get_out_neighbors(spiker)
    
    nbsize = len(nbs)
    
    if nbsize != 0:
        spread_val = spiker_activation/nbsize
        for nb in nbs:
            w = g.ep.weight((spiker, nb))
            g.vp.activation[nb] += spread_val*w
            g.vp.activation(spiker) -= spread_val*w
    else:
        if g.vp.activation[spiker] >= 1:

            def get_closest_nonnb(v):
                check = False
                # chosen = None
                nth_nbs = g.get_all_neighbors(g.get_in_neighbors(v))
                while not check:
                    # chosen = npr.choice(nth_nbs)

                    for nthnb in nth_nbs:
                        nthnb_edges = set(g.get_edges(nthnb))
                        
                        if not((v, nthnb) in nthnb_edges
                            or (nthnb, v) in nthnb_edges):
                            
                            g.add_edge(v, nthnb)
                            return

                    nth_nbs = g.get_all_neighbors(nth_nbs)        
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
g = set_graph()
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
