import geopandas
import numpy
import numpy.random
import queue
import time
import os
import json
import random
from multiprocessing import Pool

def check_pew_rm(seats_gpdf, allocated_seats, available_seats):
    pews_to_chk = list()
    for seat in allocated_seats:
        pew = seats_gpdf.loc[seats_gpdf['seat_id'] == seat]
        pew_id = pew.iloc[0]['pew_id']
        if pew_id not in pews_to_chk:
            pews_to_chk.append(pew_id)
    
    for pew in pews_to_chk:
        pew_seats = seats_gpdf.loc[seats_gpdf['pew_id'] == pew]
        for idx in range(pew_seats.shape[0]):
            seat_id = pew_seats.iloc[idx]['seat_id']
            available_seats = available_seats[available_seats != seat_id]
            seats_gpdf.loc[seats_gpdf['seat_id'] == seat_id, 'available_seats'] = 0
    return available_seats, seats_gpdf


def is_seat_avail(seat, seats_gpdf):
    seat_avail = False
    if seats_gpdf.loc[seats_gpdf['seat_id'] == seat, 'available_seats'].iloc[0] == 1:
        pew = seats_gpdf.loc[seats_gpdf['seat_id'] == seat].iloc[0]['pew_id']
        seat_dists = seats_gpdf.loc[seats_gpdf['allocated_seats'] == 1].loc[seats_gpdf['pew_id'] != pew]['dist_{}'.format(seat)]
        if seat_dists.min() > 1950:
            seat_avail = True
    return seat_avail


# A function to allocate a seat/pew.
def allocate_seats_pew(init_seat, allocate_n_seats, seats_gpdf, allocated_seats, available_seats):
    seat_allocated = False
    seat_avail = is_seat_avail(init_seat, seats_gpdf)
    if seat_avail:
        seats = list()
        seats.append(init_seat)
        
        if allocate_n_seats > 1:
            visited = list()
            visited.append(init_seat)
            neighs = queue.SimpleQueue()
            l_neigh = seats_gpdf.loc[seats_gpdf['seat_id'] == init_seat].iloc[0]['neighs_left']
            r_neigh = seats_gpdf.loc[seats_gpdf['seat_id'] == init_seat].iloc[0]['neighs_right']
            if l_neigh > 0:
                neighs.put(l_neigh)
            if r_neigh > 0:
                neighs.put(r_neigh)

            while (not neighs.empty()):
                c_neigh = neighs.get()
                seat_avail = is_seat_avail(c_neigh, seats_gpdf)
                if seat_avail:
                    seats.append(c_neigh)
                    visited.append(c_neigh)
                    l_neigh = seats_gpdf.loc[seats_gpdf['seat_id'] == c_neigh].iloc[0]['neighs_left']
                    r_neigh = seats_gpdf.loc[seats_gpdf['seat_id'] == c_neigh].iloc[0]['neighs_right']
                    if (l_neigh > 0) and (l_neigh not in visited):
                        neighs.put(l_neigh)
                    if (r_neigh > 0) and (r_neigh not in visited):
                        neighs.put(r_neigh)
                if len(seats) == allocate_n_seats:
                    break
        
        if len(seats) == allocate_n_seats:
            print(seats)
            for allo_seat in seats:
                allocated_seats.append(allo_seat)
                seats_gpdf.loc[seats_gpdf['seat_id'] == allo_seat, 'allocated_seats'] = 1

                available_seats = available_seats[available_seats != allo_seat]
                seats_gpdf.loc[seats_gpdf['seat_id'] == allo_seat, 'available_seats'] = 0

                seat_allocated = True
                
    else:
        available_seats = available_seats[available_seats != init_seat]
        seats_gpdf.loc[seats_gpdf['seat_id'] == init_seat, 'available_seats'] = 0
    
    return seat_allocated, seats_gpdf, allocated_seats, available_seats


def find_n_seats(n_pews_for, grp_n_seats, max_iters, gpdf_all, allocated_seats, available_seats, rn_gen):
    n_allocations = 0
    n_iters = 0
    while n_allocations < n_pews_for:
        n_seats = len(available_seats)
        seat_idx = rn_gen.integers(low=0, high=n_seats, size=1)[0]
        seat_id = available_seats[seat_idx]
        seat_allocated, seats_gpdf, allocated_seats, available_seats = allocate_seats_pew(available_seats[seat_idx], grp_n_seats, gpdf_all, allocated_seats, available_seats)
        if seat_allocated:
            print("Seat {} Allocated".format(seat_id))
            available_seats, gpdf_all = check_pew_rm(gpdf_all, allocated_seats, available_seats)
            n_allocations = n_allocations + 1
        #print("n_allocations: ", n_allocations)
        #print("\tlen(allocated_seats): ", len(allocated_seats))
        #print("\tlen(available_seats): ", len(available_seats))
        n_iters = n_iters + 1
        if n_iters > max_iters:
            break
    return gpdf_all, allocated_seats, available_seats



def allocate_avail_seats(grp_n_seats, max_iters, gpdf_all, allocated_seats, available_seats, rn_gen):
    n_allocations = 0
    n_iters = 0
    while len(available_seats) > 0:
        n_seats = len(available_seats)
        seat_idx = rn_gen.integers(low=0, high=n_seats, size=1)[0]
        seat_id = available_seats[seat_idx]
        seat_allocated, seats_gpdf, allocated_seats, available_seats = allocate_seats_pew(available_seats[seat_idx], grp_n_seats, gpdf_all, allocated_seats, available_seats)
        if seat_allocated:
            print("Seat {} Allocated".format(seat_id))
            available_seats, gpdf_all = check_pew_rm(gpdf_all, allocated_seats, available_seats)
            n_allocations = n_allocations + 1
        #print("n_allocations: ", n_allocations)
        #print("\tlen(allocated_seats): ", len(allocated_seats))
        #print("\tlen(available_seats): ", len(available_seats))
        n_iters = n_iters + 1
        if n_iters > max_iters:
            break
    return gpdf_all, allocated_seats, available_seats

    
    
def test_all_available_seats(gpdf_all, allocated_seats, available_seats):
    seats_allocated = list()
    for seat in available_seats:
        if is_seat_avail(seat, gpdf_all):
            seats_allocated.append(seat)
            print("Seat {} Allocated".format(seat))
            gpdf_all.loc[gpdf_all['seat_id'] == seat, 'allocated_seats'] = 1
            gpdf_all.loc[gpdf_all['seat_id'] == seat, 'available_seats'] = 0
            allocated_seats.append(seat)
        
    available_seats = list()
        
    return gpdf_all, allocated_seats, available_seats


def reset_available_seats(gpdf_all):
    gpdf_all['available_seats'] = numpy.ones(gpdf_all.shape[0])
    gpdf_all.loc[gpdf_all['allocated_seats'] == 1, 'available_seats'] = 0
    
    available_seats = numpy.array(gpdf_all.loc[gpdf_all['available_seats'] == 1]['seat_id'])
    
    return gpdf_all, available_seats 


def seat_plan_metrics(gpdf, allo_seats_col, pew_id_col, seat_id_col):    
    pew_ids = numpy.array(gpdf.loc[gpdf[allo_seats_col] == 1][pew_id_col])
    seat_ids = numpy.array(gpdf.loc[gpdf[allo_seats_col] == 1][seat_id_col])
    
    pew_ids = numpy.unique(pew_ids)
    
    n_pews = pew_ids.shape[0]
    n_seats = seat_ids.shape[0]
    
    seats_metric = n_pews * n_seats
    
    return n_pews, n_seats, seats_metric


def run_seat_allocation_analysis(seed, in_vec_file, in_vec_lyr, out_vec_file, out_metrics_file):
    rn_gen = numpy.random.default_rng(seed)
    
    gpdf_all = geopandas.read_file(in_vec_file, layer=in_vec_lyr)
    
    gpdf_all['allocated_seats'] = gpdf_all['reserved_seats']
    gpdf_all['available_seats'] = numpy.zeros(gpdf_all.shape[0])
    
    gpdf_all.loc[gpdf_all['reserved_pews'] == 0, 'available_seats'] = 1
    gpdf_all.loc[gpdf_all['reserved_seats'] == 1, 'available_seats'] = 0
    
    #print(gpdf_all.loc[gpdf_all['available_seats'] == 1].shape)
    
    allocated_seats = numpy.array(gpdf_all.loc[gpdf_all['allocated_seats'] == 1]['seat_id']).tolist()
    available_seats = numpy.array(gpdf_all.loc[gpdf_all['available_seats'] == 1]['seat_id'])
    available_seats, gpdf_all = check_pew_rm(gpdf_all, allocated_seats, available_seats)
    
    pews_for_5 = 2
    pews_for_4 = 4
    pews_for_3 = 2
    
    gpdf_all, allocated_seats, available_seats = find_n_seats(pews_for_5, 5, 10, gpdf_all, allocated_seats, available_seats, rn_gen)
    gpdf_all, allocated_seats, available_seats = find_n_seats(pews_for_4, 4, 10, gpdf_all, allocated_seats, available_seats, rn_gen)
    gpdf_all, allocated_seats, available_seats = find_n_seats(pews_for_3, 3, 10, gpdf_all, allocated_seats, available_seats, rn_gen)
    gpdf_all, available_seats = reset_available_seats(gpdf_all)
    gpdf_all, allocated_seats, available_seats = allocate_avail_seats(2, 250, gpdf_all, allocated_seats, available_seats, rn_gen)
    gpdf_all, available_seats = reset_available_seats(gpdf_all)
    gpdf_all, allocated_seats, available_seats = test_all_available_seats(gpdf_all, allocated_seats, available_seats)
    
    n_pews, n_seats, seats_metric = seat_plan_metrics(gpdf_all, 'allocated_seats', 'pew_id', 'seat_id')
    
    out_vec_path = os.path.splitext(os.path.basename(out_vec_file))[0]
    out_info = dict()
    out_info[out_vec_path] = dict()
    out_info[out_vec_path]['vec_file'] = out_vec_file
    out_info[out_vec_path]['vec_lyr'] = out_vec_path
    out_info[out_vec_path]['n_pews'] = n_pews
    out_info[out_vec_path]['n_seats'] = n_seats
    out_info[out_vec_path]['seats_metric'] = seats_metric
    
    with open(out_metrics_file, 'w') as fp:
        json.dump(out_info, fp, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    
    gpdf_all.to_file(out_vec_file, driver='GeoJSON')


def run_func(params):
    time.sleep(random.randint(1,5))
    seed = int(time.time()*10000)*random.randint(1,1000)
    run_seat_allocation_analysis(seed, params[0], params[1], params[2], params[3])


if __name__ == '__main__':
    n_exp = 1000
    run_params = list()
    for i in range(n_exp):
        run_params.append(['stmikes_seats_reserved_distmtx.geojson', 'stmikes_seats_reserved_distmtx', 'out_plans/stmikes_seats_allocated_{}.geojson'.format(i), 'out_plans/stmikes_seats_allocated_metrics_{}.json'.format(i)])
    
    
    with Pool(3) as p:
        p.map(run_func, run_params)






