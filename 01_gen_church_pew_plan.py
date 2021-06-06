import shapely.geometry
import geopandas
import pandas
import math

def create_row(pew_widths, length=800, start_x=0, start_y=10000, pew_x_off=None, person_width=500, pew_id_off=0, seat_id_off=0, seat_len=400):
    pews = list()
    pew_seats = list()
    c_start_x = start_x
    c_start_y = start_y
    i = 0
    j = 0
    pew_id = list()
    seat_id = list()
    neigh_left = list()
    neigh_right = list()
    for pew_width in pew_widths:
        n_seats = int(math.floor(pew_width/person_width))
        
        if pew_x_off is None:
            tlx = c_start_x
        else:
            tlx = c_start_x + pew_x_off[i]
        tly = c_start_y
        
        first = True
        for n_seat in range(n_seats):
            
            ctlx = tlx + (person_width * n_seat)
            
            brx = ctlx + person_width
            bry = tly - length
        
            pews.append(shapely.geometry.Polygon([(ctlx, tly), (brx, tly), (brx, bry), (ctlx, bry), (ctlx, tly)]))
            
            pew_seats.append(shapely.geometry.Polygon([(ctlx, bry+seat_len), (brx, bry+seat_len), (brx, bry), (ctlx, bry), (ctlx, bry+seat_len)]))
            
            pew_id.append(i+1+pew_id_off)
            seat_id.append(j+1+seat_id_off)
            
            if first:
                neigh_left.append(0)
                first = False
            else:
                neigh_left.append(j+seat_id_off)
                
            if (n_seat+1) == n_seats:
                neigh_right.append(0)
                first = False
            else:
                neigh_right.append(j+2+seat_id_off)
            
            j = j + 1
            
        
        c_start_y = bry
        i = i + 1
        
        
    gpdf_pews = geopandas.GeoDataFrame(columns=['geometry'], data=pews, crs='EPSG:27700')
    gpdf_pews['pew_id'] = pew_id
    gpdf_pews['seat_id'] = seat_id
    gpdf_pews['neighs_left'] = neigh_left
    gpdf_pews['neighs_right'] = neigh_right
    #gpdf_pews.set_crs(epsg=27700)
    
    gpdf_pew_seats = geopandas.GeoDataFrame(columns=['geometry'], data=pew_seats, crs='EPSG:27700')
    gpdf_pew_seats['pew_id'] = pew_id
    gpdf_pew_seats['seat_id'] = seat_id
    gpdf_pew_seats['neighs_left'] = neigh_left
    gpdf_pew_seats['neighs_right'] = neigh_right
    #gpdf_pew_seats.set_crs(epsg=27700)
        
    return gpdf_pews, gpdf_pew_seats


pew_id_off = 0
seat_id_off = 0


pew_widths = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000]
gpdf_pews_1, gpdf_pew_seats_1 = create_row(pew_widths, length=850, start_x=0, start_y=10000, pew_id_off=pew_id_off, seat_id_off=seat_id_off)
pew_id_off = pew_id_off + gpdf_pews_1.pew_id.unique().shape[0]
seat_id_off = seat_id_off + gpdf_pews_1.shape[0]


pew_widths = [2000, 3000, 3000, 3000, 2000, 2000, 3000, 3000, 3000, 2000]
gpdf_pews_2, gpdf_pew_seats_2 = create_row(pew_widths, length=850, start_x=3900, start_y=10000, pew_id_off=pew_id_off, seat_id_off=seat_id_off)
pew_id_off = pew_id_off + gpdf_pews_2.pew_id.unique().shape[0]
seat_id_off = seat_id_off + gpdf_pews_2.shape[0]

pew_widths = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000]
gpdf_pews_3, gpdf_pew_seats_3 = create_row(pew_widths, length=850, start_x=6900, start_y=10000, pew_id_off=pew_id_off, seat_id_off=seat_id_off)
pew_id_off = pew_id_off + gpdf_pews_3.pew_id.unique().shape[0]
seat_id_off = seat_id_off + gpdf_pews_3.shape[0]

pew_widths = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000]
gpdf_pews_4, gpdf_pew_seats_4 = create_row(pew_widths, length=850, start_x=11300, start_y=10000, pew_id_off=pew_id_off, seat_id_off=seat_id_off)
pew_id_off = pew_id_off + gpdf_pews_4.pew_id.unique().shape[0]
seat_id_off = seat_id_off + gpdf_pews_4.shape[0]

pew_widths = [2000, 2000, 3000, 3000, 2000, 2000, 3000, 3000, 3000, 2000, 2000]
pew_x_off = [1000, 1000, 0, 0, 1000, 1000, 0, 0, 0, 1000, 1000]
gpdf_pews_5, gpdf_pew_seats_5 = create_row(pew_widths, length=850, start_x=14300, start_y=10000, pew_x_off=pew_x_off, pew_id_off=pew_id_off, seat_id_off=seat_id_off)
pew_id_off = pew_id_off + gpdf_pews_5.pew_id.unique().shape[0]
seat_id_off = seat_id_off + gpdf_pews_5.shape[0]

pew_widths = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000]
gpdf_pews_6, gpdf_pew_seats_6 = create_row(pew_widths, length=850, start_x=18200, start_y=10000, pew_id_off=pew_id_off, seat_id_off=seat_id_off)


gpdf_pews = pandas.concat([gpdf_pews_1, gpdf_pews_2, gpdf_pews_3, gpdf_pews_4, gpdf_pews_5, gpdf_pews_6])
gpdf_pew_seats = pandas.concat([gpdf_pew_seats_1, gpdf_pew_seats_2, gpdf_pew_seats_3, gpdf_pew_seats_4, gpdf_pew_seats_5, gpdf_pew_seats_6])

gpdf_pews.to_file('stmikes_pews_base.geojson', driver='GeoJSON')

gpdf_pew_seats.to_file('stmikes_seats_base.geojson', driver='GeoJSON')


