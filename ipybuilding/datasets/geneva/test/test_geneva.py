import os

import geopandas

from ipybuilding.datasets import geneva

start_point = (6.1402, 46.208742)
delta = 0.001
bbox = (
    start_point[0] - delta,
    start_point[1] - delta,
    start_point[0] + delta,
    start_point[1] + delta,
)


def test_geneva_load_data():
    file_paths = geneva.load_data()
    for path in file_paths:
        assert os.path.isfile(path)
        bases = geopandas.read_file(path, bbox=bbox)
