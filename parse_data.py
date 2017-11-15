#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import scipy.interpolate

def interpolate_points(grid_x, grid_y, x, y, values, method='linear'):
    """
    Interpolate points into DataArray
    
    grid_x: X axis of the grid
    grid_y: Y axis of the grid
    x: X value of each point
    y: Y value of each point
    values: Value at each point
    method: scipy.interpolate.griddata method to use
    """

    array = scipy.interpolate.griddata(
            (x, y),
            values,
            (grid_x, grid_y),
            method=method)

    darray = xr.DataArray(
            array,
            coords=[x, y],
            dims=['x', 'y'])

    return darray


def main():
    dtype = [
            ('x', np.float64),
            ('y', np.float64),
            ('ux', np.float64),
            ('uy', np.float64)
        ]

    with open('data.txt') as f:
        data = np.loadtxt(f, dtype=dtype)

    data = np.unique(data)
    x = data['x']
    y = data['y']
    ux = data['ux']
    uy = data['uy']

    X, Y = np.meshgrid(x, y)
    da = interpolate_points(X, Y, x, y, uy)

    plt.figure()
    plt.axes().set_aspect('equal', 'datalim')
    plt.contourf(X, Y, da, origin='lower')
    plt.colorbar()
    plt.scatter(x, y, marker='o', c='b', s=5)
    plt.show()


if __name__ == "__main__":
    main()
