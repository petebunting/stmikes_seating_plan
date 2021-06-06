import geopandas
import numpy

gpdf = geopandas.read_file('stmikes_seats_reserved_distmtx.geojson', layer='stmikes_seats_reserved_distmtx')

allocated_pews = [3, 6, 9, 10, 13, 16, 19, 22, 25, 28, 31, 32, 35, 38, 41, 45, 48, 51, 54, 55, 58, 61, 64, 67, 68, 69]

n_seats = gpdf.shape[0]

gpdf['allocated_pews_c'] = numpy.zeros(n_seats)

for pew in allocated_pews:
    gpdf.loc[gpdf['pew_id']==pew, 'allocated_pews_c'] = 1
    
gpdf['allocated_seats_c'] = gpdf['allocated_pews_c']
    
#for seat in reserved_seats:
#    gpdf.loc[gpdf['seat_id']==seat, 'reserved_seats'] = 1

gpdf.to_file('stmikes_seats_current_pews.geojson', driver='GeoJSON')
