[![Documentation Status](https://readthedocs.org/projects/ipybuilding/badge/?version=main)](https://ipybuilding.readthedocs.io/en/main)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# ipybuilding: 3D interactive urban visualisation in Jupyter notebooks

ipybuilding is a collection of code and examples for visualising 3D building data and overlay information in Jupyter notebooks.

Pydeck provides an ipython widget for the deck.gl 3D visualisatin toolkit. 

Several geospatial data sources provide 3D building data, in this case we use data from the Geneva open access cartography service. This was originally provided in GML format and converted to Geopackage (gpkg).

Using geopandas we can load the 3D geo-polygon data and associate it with other information for visualisation, and display this in an interactive 3D visualisation.
