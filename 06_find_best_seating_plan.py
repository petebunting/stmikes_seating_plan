import geopandas
import numpy
import glob
import os
import tqdm
import json

def seat_plan_metrics(vec_file, vec_lyr, allo_seats_col, pew_id_col, seat_id_col):
    gpdf = geopandas.read_file(vec_file, layer=vec_lyr, usecols=[allo_seats_col, pew_id_col, seat_id_col])
    
    pew_ids = numpy.array(gpdf.loc[gpdf[allo_seats_col] == 1][pew_id_col])
    seat_ids = numpy.array(gpdf.loc[gpdf[allo_seats_col] == 1][seat_id_col])
    
    pew_ids = numpy.unique(pew_ids)
    
    n_pews = pew_ids.shape[0]
    n_seats = seat_ids.shape[0]
    
    seats_metric = n_pews * n_seats
    
    return n_pews, n_seats, seats_metric



vec_files = glob.glob("out_plans/*.geojson")

out_info = dict()
for vec_file in tqdm.tqdm(vec_files):
    vec_lyr = os.path.splitext(os.path.basename(vec_file))[0]
    #print(vec_file)
    #print(vec_lyr)

    n_pews, n_seats, seats_metric = seat_plan_metrics(vec_file, vec_lyr, 'allocated_seats', 'pew_id', 'seat_id')
    
    #print("n_pews = {}".format(n_pews))
    #print("n_seats = {}".format(n_seats))
    #print("seats_metric = {}".format(seats_metric))
    
    out_info[vec_lyr] = dict()
    out_info[vec_lyr]['vec_file'] = vec_file
    out_info[vec_lyr]['vec_lyr'] = vec_lyr
    out_info[vec_lyr]['n_pews'] = n_pews
    out_info[vec_lyr]['n_seats'] = n_seats
    out_info[vec_lyr]['seats_metric'] = seats_metric
    
    
with open('./seat_plan_metrics.json', 'w') as fp:
    json.dump(out_info, fp, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)




