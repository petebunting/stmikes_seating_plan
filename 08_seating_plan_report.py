import geopandas
import numpy


def find_closest_seat(gpdf, seat, allo_seats_col, pew_id_col, seat_id_col):
    pew = gpdf.loc[gpdf[seat_id_col] == seat].iloc[0][pew_id_col]
    seat_dists = gpdf.loc[gpdf[allo_seats_col] == 1].loc[gpdf[pew_id_col] != pew]['dist_{}'.format(seat)]
    return seat_dists.min()

def seat_plan_report(vec_file, vec_lyr, allo_seats_col, pew_id_col, seat_id_col, print_seat_dists=True):
    gpdf = geopandas.read_file(vec_file, layer=vec_lyr)
    
    pew_ids = numpy.array(gpdf.loc[gpdf[allo_seats_col] == 1][pew_id_col])
    seat_ids = numpy.array(gpdf.loc[gpdf[allo_seats_col] == 1][seat_id_col])
    
    pew_ids = numpy.unique(pew_ids)
    
    n_pews = pew_ids.shape[0]
    n_seats = seat_ids.shape[0]
    
    seats_metric = n_pews * n_seats
    
    n_invalid_dists = 0
    print("Number of Pews: {}".format(n_pews))
    print("Number of Seats: {}".format(n_seats))
    if print_seat_dists:
        print("Seat Min Distances (metres):")
        for seat in seat_ids:
            min_dist = find_closest_seat(gpdf, seat, allo_seats_col, pew_id_col, seat_id_col)
            print("\tSeat {}: {}".format(seat, round(min_dist/1000.0, 2)))
            if min_dist < 1950:
                n_invalid_dists += 1
        if n_invalid_dists > 0:
            print("**** WARNING ****")
            print("There are {} seats which are too close to another allocated seat.".format(n_invalid_dists))

    

top_10_lyrs = ['stmikes_seats_allocated_53', 'stmikes_seats_allocated_26', 'stmikes_seats_allocated_105', 'stmikes_seats_allocated_116', 'stmikes_seats_allocated_121', 'stmikes_seats_allocated_30', 'stmikes_seats_allocated_60', 'stmikes_seats_allocated_170', 'stmikes_seats_allocated_178', 'stmikes_seats_allocated_196', 'stmikes_seats_allocated_235']

for lyr in top_10_lyrs:
    print(lyr)
    seat_plan_report('out_plans/{}.geojson'.format(lyr), lyr, 'allocated_seats', 'pew_id', 'seat_id', print_seat_dists=False)


#seat_plan_report('out_plans/stmikes_seats_allocated_53.geojson', 'stmikes_seats_allocated_53', 'allocated_seats', 'pew_id', 'seat_id', print_seat_dists=False)


#seat_plan_report('stmikes_seats_current_pews.geojson', 'stmikes_seats_current_pews', 'allocated_seats_c', 'pew_id', 'seat_id', print_seat_dists=False)
#seat_plan_report('stmikes_seats_current_pews_covid.geojson', 'stmikes_seats_current_pews_covid', 'allocated_seats_c', 'pew_id', 'seat_id', print_seat_dists=False)



