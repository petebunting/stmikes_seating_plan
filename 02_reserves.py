import geopandas
import numpy

gpdf = geopandas.read_file('stmikes_seats_base.geojson', layer='stmikes_seats_base')

#reserved_pews = [2, 4, 6, 8, 
#                 10, 12, 14, 16, 18, 
#                 21, 23, 25, 27, 29, 31,
#                 32, 34, 36, 38, 40, 42, 
#                 44, 46, 48, 50, 52, 54,
#                 56, 58, 60, 62, 64, 66]

reserved_seats = [255, 256, 257]

n_seats = gpdf.shape[0]

gpdf['reserved_pews'] = numpy.zeros(n_seats)
gpdf['reserved_seats'] = numpy.zeros(n_seats)


#for pew in reserved_pews:
#    gpdf.loc[gpdf['pew_id']==pew, 'reserved_pews'] = 1
    
for seat in reserved_seats:
    gpdf.loc[gpdf['seat_id']==seat, 'reserved_seats'] = 1

gpdf.to_file('stmikes_seats_reserved.geojson', driver='GeoJSON')
