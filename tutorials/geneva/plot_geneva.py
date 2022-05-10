"""
Geneva
===================================
In this tutorial, we will learn how to load Geneva 3D buildings datasets.
"""

#%%
# Geneva Geneva 3D buildings datasets can be loaded thanks to the geneva.load_data()
# function.
# This function will first check if the city's building geometries files are already
# present in the dataset folder.
# You can acces the local geneva dataset directory using the following function:

from ipybuilding.utils import get_config

config = get_config()
path = config["GENEVA_DATASET_PATH"]
path

#If not already present on your computer, this function will automatically
# download the 3 .gpkg files containing the city building's geometries from a remote serveur
# and save them in the local geneva dataset directory for futur use.
# If the file are already present in the local geneva dataset directory, the function will
# check the hash in case of modification and redownload clean versions if needed.

from ipybuilding.datasets import geneva

base_path, facade_path, roof_path = geneva.load_data()
base_path
#%%
# base_path, facade_path, roof_path are the respective path to the files
# of base, roof and facade geometries of geneva's buildings.
# theses files can esaly be loaded thanks to geopandas:

import geopandas
bases = geopandas.read_file(base_path)
bases