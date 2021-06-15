
# %%

import graph_tool.all as gt
import numpy as np
import numpy.random as npr
# import matplotlib.colors as mplc
from matplotlib import cm
import matplotlib.colors as mplc
import os, sys
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib
from scipy.fftpack import cc_diff
from plot_functions import *


# %%


g = gt.random_graph(100, lambda: (2, 2))

tree = gt.min_spanning_tree(g)

g.set_edge_filter(tree)

root = [v for v in g.vertices() if v.in_degree() == 0]

# %%

root

# %%
dom = gt.dominator_tree(g, root[9])

print(dom.a)
# %%

# %%
gt.graph_draw(g, vertex_fill_color=dom, vertex_size=7)
# %%
