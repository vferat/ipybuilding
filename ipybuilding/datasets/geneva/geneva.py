"""Functions to use the Geneva dataset."""

import os

import pkg_resources as pkr
import pooch

from ...utils._config import get_config


def load_data():
    """
    Get path to local copy of Geneva dataset.
    Returns
    -------
    path : str
        path to local copy of the requested data.
    """  # noqa

    config = get_config()
    path = config["GENEVA_DATASET_PATH"]
    fetcher = pooch.create(
        path=path,
        base_url=rf"https://drive.switch.ch/index.php/s/OVjDG0Ae03jYlJm/download?path=%2F&files=",  # noqa,
        version=None,
        registry=None,
    )
    registry = pkr.resource_stream(
        "ipybuilding",
        os.path.join("datasets", "geneva", "data", "registry.txt"),
    )

    fetcher.load_registry(registry)

    base_filename = "bases.gpkg"
    base_filename = fetcher.fetch(base_filename)

    facades_filename = "facades.gpkg"
    facades_filename = fetcher.fetch(facades_filename)

    toits_filename = "toits.gpkg"
    toits_filename = fetcher.fetch(toits_filename)

    return base_filename, facades_filename, toits_filename
