import numpy as np
import xarray as xr

from nowcast import extract_rows, validate_forecast_rows


def make_dataset(times):
    lat = xr.DataArray([[52.0, 52.0], [52.2, 52.2]], dims=("y", "x"), name="latitude")
    lon = xr.DataArray([[5.2, 5.4], [5.2, 5.4]], dims=("y", "x"), name="longitude")
    threshold = np.array([0.1, 1.0, 3.0])
    values = np.zeros((len(times), 3, 2, 2), dtype=float)
    values[:, :, 1, 1] = np.array([[0.8, 0.5, 0.1]])
    return xr.Dataset(
        {"precipitation_exceedance_probability": (("time", "threshold", "y", "x"), values)},
        coords={"time": times, "threshold": threshold, "latitude": lat, "longitude": lon},
    )


def test_basic_probability_extraction():
    time = np.array(["2026-08-28T13:00", "2026-08-28T13:05"], dtype="datetime64[m]")
    ds = make_dataset(time)
    var, point, rows = extract_rows(ds, 52.18, 5.39, 10)
    assert var == "precipitation_exceedance_probability"
    assert point.indexers == {"y": 1, "x": 1}
    assert rows[0]["probabilities"][">=0.1 mm/h"] == 80.0
    assert rows[1]["probabilities"][">=3 mm/h"] == 10.0
    assert rows[1]["lead_minutes"] == 5.0


def test_horizon_is_derived_from_time_axis_and_includes_180_minutes():
    start = np.datetime64("2026-08-28T13:00")
    times = start + np.arange(73) * np.timedelta64(5, "m")
    ds = make_dataset(times)
    _, _, rows = extract_rows(ds, 52.18, 5.39, 180)
    assert len(rows) == 37
    assert rows[0]["lead_minutes"] == 0.0
    assert rows[-1]["lead_minutes"] == 180.0
    valid, problems = validate_forecast_rows(rows, 180)
    assert valid, problems


def test_numeric_forecast_period_in_minutes():
    lat = xr.DataArray([[52.0]], dims=("y", "x"), name="latitude")
    lon = xr.DataArray([[5.4]], dims=("y", "x"), name="longitude")
    lead = xr.DataArray(
        np.arange(0, 185, 5),
        dims=("forecast_period",),
        name="forecast_period",
        attrs={"units": "minutes", "standard_name": "forecast_period"},
    )
    values = np.full((len(lead), 1, 1), 0.25)
    ds = xr.Dataset(
        {"precipitation_probability": (("forecast_period", "y", "x"), values)},
        coords={"forecast_period": lead, "latitude": lat, "longitude": lon},
    )
    _, _, rows = extract_rows(ds, 52.0, 5.4, 180)
    assert rows[-1]["lead_minutes"] == 180.0
    assert rows[0]["probabilities"]["precipitation"] == 25.0


def test_validation_rejects_short_horizon():
    rows = [
        {"lead_minutes": 0.0, "probabilities": {"precipitation": 10.0}},
        {"lead_minutes": 175.0, "probabilities": {"precipitation": 20.0}},
    ]
    valid, problems = validate_forecast_rows(rows, 180)
    assert not valid
    assert any("stopt" in problem for problem in problems)


if __name__ == "__main__":
    test_basic_probability_extraction()
    test_horizon_is_derived_from_time_axis_and_includes_180_minutes()
    test_numeric_forecast_period_in_minutes()
    test_validation_rejects_short_horizon()
    print("synthetic core tests: OK")
