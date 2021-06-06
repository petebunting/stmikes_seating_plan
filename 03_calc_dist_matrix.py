import geopandas

gpdf = geopandas.read_file('stmikes_seats_reserved.geojson', layer='stmikes_seats_reserved')

gpdf_cp = gpdf.copy(deep=True)

gpdf_cp['geometry'] = gpdf_cp.centroid


dist = gpdf_cp.geometry.apply(lambda x: gpdf_cp.distance(x))

for idx in dist:
    gpdf['dist_{}'.format(idx+1)] = dist[idx]
    
gpdf.to_file('stmikes_seats_reserved_distmtx.geojson', driver='GeoJSON')


gpdf_cp.to_file('stmikes_seats_pts.geojson', driver='GeoJSON')
