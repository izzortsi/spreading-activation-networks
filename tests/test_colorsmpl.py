from matplotlib import cm
import matplotlib.colors as mplc
import numpy as np

cdict1 = {'red':  ((0.0, 0.0, 0.0),
                   (0.25, 0.0, 0.0),
                   (0.5, 0.8, 1.0),
                   (0.75, 1.0, 1.0),
                   (1.0, 0.4, 1.0)),

          'green': ((0.0, 0.0, 0.0),
                    (0.25, 0.0, 0.0),
                    (0.5, 0.9, 0.9),
                    (0.75, 0.0, 0.0),
                    (1.0, 0.0, 0.0)),

          'blue':  ((0.0, 0.0, 0.4),
                    (0.25, 1.0, 1.0),
                    (0.5, 1.0, 0.8),
                    (0.75, 0.0, 0.0),
                    (1.0, 0.0, 0.0))
          }

blue_red1 = mplc.LinearSegmentedColormap('BlueRed1', cdict1)


##ou

cmap = cm.get_cmap('copper', 100)

##ou, por lista
    
grad = np.linspace(0, 1, 20, endpoint=True)
colors = [(c, c, c) for c in grad]
cmap = mplc.LinearSegmentedColormap.from_list("gscale", colors, N=20)


grad_scale = np.logspace(-2, 2, 100, endpoint=True)/10
viridis = cm.get_cmap('blue', 100)
newcolors = viridis(grad_scale)
# %%


# %%

viridis
# %%
newcolors

# %%

cmap = mplc.LinearSegmentedColormap.from_list("gscale", newcolors)
# %%
cmap