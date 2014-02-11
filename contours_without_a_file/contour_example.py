import aplpy
import numpy as np
from matplotlib import pyplot as plt

# Load up stars
ra,dec = np.loadtxt('../data/sources.txt').T
grid,yedges,xedges = np.histogram2d(ra,dec,bins=(np.linspace(265.83,266.97,100),np.linspace(-29.43,-28.43,100)))
xcenters = (xedges[1:] + xedges[:-1])/2.
ycenters = (yedges[1:] + yedges[:-1])/2.
Xgrid, Ygrid = np.meshgrid(ycenters, xcenters)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

CS = plt.contour(Xgrid, Ygrid, grid, extent=extent, levels=np.logspace(0,2,11))


def get_contour_verts(cn):
    contours = []
    # for each contour line
    for cc in cn.collections:
        paths = []
        # for each separate section of the contour line
        for pp in cc.get_paths():
            xy = []
            # for each segment of that section
            for vv in pp.iter_segments():
                xy.append(vv[0])
            paths.append(np.vstack(xy))
        contours.append(paths)

    return contours

contours = get_contour_verts(CS)


F = aplpy.FITSFigure('../data/2MASS_k.fits.gz')
F.show_grayscale()

for ii,contours_at_level in enumerate(contours):
    clines = [cl.T for cl in contours_at_level]
    F.show_lines(clines,zorder=10,layer='contour_level_%i' % ii,color='r')

F.refresh()

F.save('external_contour_example.png')
