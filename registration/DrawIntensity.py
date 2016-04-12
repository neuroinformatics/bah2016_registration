# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:10:16 2016
based on http://qiita.com/s-wakaba/items/a93f03f27137cff4a26c

@author: nebula
"""
import numpy as np
import csv
from pandas import DataFrame
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, dendrogram


GREEN_CMAP = LinearSegmentedColormap('green', {
    'red': [(0.0, 0.0, 0.0), (0.3, 0.2, 0.2), (1.0, 0.0, 0.0)],
    'green': [(0.0, 0.0, 0.0), (0.3, 0.5, 0.5), (1.0, 1.0, 1.0)],
    'blue': [(0.0, 0.0, 0.0), (0.3, 0.2, 0.2), (1.0, 0.0, 0.0)],
})

RED_CMAP = LinearSegmentedColormap('green', {
    'red': [(0.0, 0.0, 0.0), (0.3, 0.5, 0.5), (1.0, 1.0, 1.0)],
    'green': [(0.0, 0.0, 0.0), (0.3, 0.2, 0.2), (1.0, 0.0, 0.0)],
    'blue': [(0.0, 0.0, 0.0), (0.3, 0.2, 0.2), (1.0, 0.0, 0.0)],
})


LABEL_NAMES = [\
'background',
'olfactory bulb',
'cerebral cortex',
'lateral septal nuclei',
'striatum',
'globus pallidus',
'thalamus',
'hypothalamus',
'hippocampal formation',
'superior colliculus',
'inferior colliculus',
'cerebellum',
'fimbria',
'internal capsule',
'ventricle',
'corpus callosum',
'subcommissural organ',
'anterior commissure',
'paraflocculus',
'deep mesencephalic nucleus',
'fornix',
'aqueaduct',
'spinal cord',
'pineal gland',
'substantia nigra',
'brainstem (remainder)',
'pontine gray',
'fasciculus retroflexus',
'amygdala',
'interpeduncular nucleus',
'periacueductal gray',
'nucleus accumbens',
'optic nerve',
'optic chiasm',
'supraoptic decussation',
'optic tract',
'lateral lemniscus',
'epithalamus',
'mammillary nucleus',
'cochlear nuclei and nerve',
]

def draw_intensity(a, cmap=GREEN_CMAP, metric='euclidean', method='average', sort_x=True, sort_y=True):

    main_axes = plt.gca()
    divider = make_axes_locatable(main_axes)

    if sort_x is True:
        plt.sca(divider.append_axes("top", 0.5, pad=0))
        xlinkage = linkage(pdist(a.T, metric=metric), method=method, metric=metric)
        xdendro = dendrogram(xlinkage, orientation='top', no_labels=True,
                             distance_sort='descending',
                             link_color_func=lambda x: 'black')
        plt.gca().set_axis_off()
        a = a[[a.columns[i] for i in xdendro['leaves']]]
    
    if sort_y is True:
        plt.sca(divider.append_axes("left", 1.0, pad=0))
        ylinkage = linkage(pdist(a, metric=metric), method=method, metric=metric)
        ydendro = dendrogram(ylinkage, orientation='right', no_labels=True,
                             distance_sort='descending',
                             link_color_func=lambda x: 'black')
        plt.gca().set_axis_off()
        a = a.ix[[a.index[i] for i in ydendro['leaves']]]
        
    plt.sca(main_axes)
    plt.imshow(a, aspect='auto', interpolation='none',
               cmap=cmap, vmin=0.0, vmax=1.0)
    plt.colorbar(pad=0.15)
    plt.gca().yaxis.tick_right()
    plt.xticks(range(a.shape[1]), a.columns, rotation=90, size='small')
    plt.yticks(range(a.shape[0]), a.index, size='x-small')
    plt.gca().xaxis.set_ticks_position('none')
    plt.gca().yaxis.set_ticks_position('none')
    plt.gca().invert_yaxis()

    plt.show()
    
    
def read_file(filename):
    intensity = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            intensity.append(row)
            
    return intensity
    
    
if __name__ == '__main__':
    N_DATA = 1000

    #intensity = read_file('../private/cx_expression.txt')
    intensity = read_file('../private/intensity_all.txt')
    Z = []
    genename = []
    for record in intensity:
        genename.append(record[0])
        Z.append([float(x) for x in record[1:41]])

    genename = genename[0:N_DATA]
    Z = np.array(Z[0:N_DATA])
    
    a = DataFrame(Z, index=genename, columns=LABEL_NAMES)
    draw_intensity(a, sort_x=False, sort_y=False, cmap=GREEN_CMAP)
    draw_intensity(a, sort_x=False, cmap=GREEN_CMAP)
    draw_intensity(a, sort_x=True, cmap=GREEN_CMAP)
    
    
    intensity = read_file('../private/cx_expression.txt')
    Z = []
    genename = []
    for record in intensity:
        genename.append(record[0])
        Z.append([float(x) for x in record[1:41]])

    genename = genename[0:N_DATA]
    Z = np.array(Z[0:N_DATA])
    
    a = DataFrame(Z, index=genename, columns=LABEL_NAMES)
    draw_intensity(a, sort_x=False, sort_y=False, cmap=RED_CMAP)
    draw_intensity(a, sort_x=False, cmap=RED_CMAP)
    draw_intensity(a, sort_x=True, cmap=RED_CMAP)
    

    