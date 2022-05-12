"""
Geneva
===================================
In this tutorial, we will learn how to display Geneva heat demand data in 3D.
"""

#%%
# We first import geneva's 3D buildings datasets
from ipybuilding.datasets import geneva

base_path, facade_path, roof_path = geneva.load_data()
#%%
# Then load them with geopandas

import geopandas

bases = geopandas.read_file(base_path)
facade = geopandas.read_file(facade_path)
toits = geopandas.read_file(roof_path)

bases.columns = [s.lower() for s in bases.columns]
facade.columns = [s.lower() for s in facade.columns]
toits.columns = [s.lower() for s in toits.columns]

#%%
# Next step is to load Geneva's heat demand data
import pandas as pd

path = '../ipybuilding/datasets/geneva/data/SCANE_INDICE_DERNIER.csv'
heat_demand = pd.read_csv(path, sep=';')
heat_demand.columns = [s.lower() for s in heat_demand.columns]
heat_demand.egid = heat_demand.egid.astype(int)

#%%
# We then merge both datasets based on bulding's EGID

bases = bases.merge(heat_demand, on='egid')
facade = facade.merge(heat_demand, on='egid')
toits = toits.merge(heat_demand, on='egid')

#%%
# We create a new column to store buidling colors based on heat demand indice:
import matplotlib as mpl

norm = mpl.colors.Normalize(vmin=1, vmax=toits.indice.quantile(0.95))
cmap = mpl.cm.get_cmap('RdYlGn_r')

cmap_val = cmap(norm(toits.indice)) 
bases['color'] = (cmap_val* 255).astype(int).tolist()

cmap_val = cmap(norm(toits.indice)) 
toits['color'] = (cmap_val* 255).astype(int).tolist()

cmap_val = cmap(norm(facade.indice)) 
facade['color'] = (cmap_val* 255).astype(int).tolist()


#%%
# Only display a subset of building based on initial view
def filtered_buildings_geom(bbox):
    return (bases.cx[bbox[0]: bbox[2], bbox[1]:bbox[3]],
            facade.cx[bbox[0]: bbox[2], bbox[1]:bbox[3]],
            toits.cx[bbox[0]: bbox[2], bbox[1]:bbox[3]])

start_point = (6.1402,46.208742)
delta = 0.001
bbox =  (start_point[0] - delta, start_point[1]-delta, start_point[0] + delta, start_point[1]+delta) 

f_base, f_face, f_toit = filtered_buildings_geom(bbox)
#%%
# We can now plot our data thanks to pydeck
import os
import pydeck

MAPBOX_API_KEY = os.environ["MAPBOX_API_KEY"]

coords = f_base.centroid.map(lambda p: [p.x, p.y])
INITIAL_VIEW_STATE = pydeck.data_utils.compute_view(coords.values)
INITIAL_VIEW_STATE.zoom = 16
INITIAL_VIEW_STATE.max_zoom = 16

# AWS Open Data Terrain Tiles
TERRAIN_IMAGE = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"

# Define how to parse elevation tiles
ELEVATION_DECODER = {"rScaler": 256, "gScaler": 1, "bScaler": 1 / 256, "offset": -32768}
SURFACE_IMAGE = f"https://api.mapbox.com/v4/mapbox.satellite/{{z}}/{{x}}/{{y}}@2x.png?access_token={MAPBOX_API_KEY}"


terrain_layer = pydeck.Layer(
    "TerrainLayer", elevation_decoder=ELEVATION_DECODER, texture=SURFACE_IMAGE, elevation_data=TERRAIN_IMAGE,
    # light_settings=lights

)


bases_layer = pydeck.Layer('GeoJsonLayer', 
                           data=f_base, get_fill_color=[255,100,255], pickable=True
                          )
facade_layer = pydeck.Layer('GeoJsonLayer', 
                            data=f_face, 
                            get_fill_color='color', 
                            line_width_scale=0.1,
                            pickable=True,
                            filled=True,
                            wireframe=True,
                           )
toits_layer = pydeck.Layer('GeoJsonLayer', 
                           data=f_toit, 
                           get_fill_color='color', 
                           pickable=True,
                           stroked=False,
                           filled=True,
                           wireframe=True,
                      )

r = pydeck.Deck(
    layers=[
        terrain_layer,
        bases_layer, 
        facade_layer, 
        toits_layer
    ],
    initial_view_state=INITIAL_VIEW_STATE,
    map_style='satellite',
    tooltip={
        'text': 'IDC: {indice} MJ/m2·a'
    }
)

r.to_HTML()