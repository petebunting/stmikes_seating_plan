import geopandas
import numpy
import numpy.random


def is_seat_avail(seat, seats_gpdf, allo_seats_col="allocated_seats"):
    seat_avail = False
    pew = seats_gpdf.loc[seats_gpdf['seat_id'] == seat].iloc[0]['pew_id']
    seat_dists = seats_gpdf.loc[seats_gpdf[allo_seats_col] == 1].loc[seats_gpdf['pew_id'] != pew]['dist_{}'.format(seat)]
    if seat_dists.min() > 1950:
        seat_avail = True
    return seat_avail



def eliminate_seats(vec_file, vec_lyr, out_vec_file, allo_seats_col="allocated_seats", seat_id_col="seat_id"):

    gpdf = geopandas.read_file(vec_file, layer=vec_lyr)
    
    seat_ids = numpy.array(gpdf.loc[gpdf[allo_seats_col] == 1][seat_id_col])
    numpy.random.shuffle(seat_ids)
    
    for seat in seat_ids:
        if seat not in [255, 256, 257]:
            if not is_seat_avail(seat, gpdf, allo_seats_col):
                print("Seat {} Not Available".format(seat))
                gpdf.loc[gpdf['seat_id'] == seat, allo_seats_col] = 0
            
    gpdf.to_file(out_vec_file, driver='GeoJSON')


eliminate_seats('stmikes_seats_current_pews.geojson', 'stmikes_seats_current_pews', out_vec_file='stmikes_seats_current_pews_covid.geojson', allo_seats_col='allocated_seats_c')

