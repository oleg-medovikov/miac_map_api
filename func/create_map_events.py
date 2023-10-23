import folium
from folium.plugins import MarkerCluster

from .create_circle import create_circle


def create_map_events(df, map_name):
    "создаем карту с кружочками экстренных случаев"
    map = folium.Map(
        name='test',
        location=[59.95020, 30.31543],
        zoom_start=11,
        max_zoom=18,
        min_zoom=10,
        min_lat=59.5,
        max_lat=60.5,
        min_lon=29.5,
        max_lon=31,
        max_bounds=True,
        prefer_canvas=True,
        tiles=None,
    )

    folium.TileLayer("CartoDB dark_matter", name=map_name).add_to(map)

    for month in df.month.unique():
        marker_cluster = MarkerCluster(
            name=month,
            overlay=True,
            control=True,
        ).add_to(map)

        for row in df.loc[df.month == month].to_dict('records'):
            circle = create_circle(row)
            circle.add_to(marker_cluster)

    folium.LayerControl().add_to(map)
    return map
