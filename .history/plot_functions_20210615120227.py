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