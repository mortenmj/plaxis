#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import scipy.interpolate


def interpolate_points(grid_x, grid_y, x, y, values, step, method='linear'):
    """
    Interpolate points into DataArray

    grid_x: X axis of the grid
    grid_y: Y axis of the grid
    x: X value of each point
    y: Y value of each point
    values: Value at each point
    method: scipy.interpolate.griddata method to use
    """
    def _interpolate(value):
        return scipy.interpolate.griddata(
                (x, y),
                value,
                (grid_x, grid_y),
                method=method)

    data = {key: (['x', 'y'], _interpolate(values[key])) for key in values}
    coords = {
            'xc': (['x', 'y'], grid_x),
            'yc': (['x', 'y'], grid_y),
            'step': step}

    ds = xr.Dataset(data, coords=coords)
    return ds


def main():
    ds = None

    xls = pd.ExcelFile('steps_result.xlsx')
    for sheet in sorted(xls.sheet_names, key=lambda x: int(x.replace("Step_",""))):
        df = xls.parse(sheet)
        df = df.drop_duplicates()

        step = int(sheet.replace("Step_", ""))
        x = df['X']
        y = df['Y']
        ux = df['Ux']
        uy = df['Uy']

        X, Y = np.meshgrid(x, y)

        values = {'ux': ux, 'uy': uy}
        tmp_ds = interpolate_points(X, Y, x, y, values, step)

        if ds is None:
            ds = tmp_ds
        else:
            ds = xr.concat([ds, tmp_ds], 'step')

    print(ds)

    plt.figure()
    ds.uy[50].plot.pcolormesh(x='xc', y='yc', add_colorbar=True)
    plt.show()


if __name__ == "__main__":
    main()
