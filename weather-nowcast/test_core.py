import numpy as np
import xarray as xr
from nowcast import extract_rows

lat = xr.DataArray([[52.0, 52.0], [52.2, 52.2]], dims=("y", "x"), name="latitude")
lon = xr.DataArray([[5.2, 5.4], [5.2, 5.4]], dims=("y", "x"), name="longitude")
time = np.array(["2026-08-28T13:00", "2026-08-28T13:05"], dtype="datetime64[m]")
threshold = np.array([0.1, 1.0, 3.0])
values = np.zeros((2, 3, 2, 2), dtype=float)
values[:, :, 1, 1] = [[0.8, 0.5, 0.1], [0.7, 0.4, 0.05]]

ds = xr.Dataset(
    {"precipitation_exceedance_probability": (("time", "threshold", "y", "x"), values)},
    coords={"time": time, "threshold": threshold, "latitude": lat, "longitude": lon},
)

var, point, rows = extract_rows(ds, 52.18, 5.39, 10)
assert var == "precipitation_exceedance_probability"
assert point.indexers == {"y": 1, "x": 1}
assert rows[0]["probabilities"][">=0.1 mm/h"] == 80.0
assert rows[1]["probabilities"][">=3 mm/h"] == 5.0
print("synthetic core test: OK")
