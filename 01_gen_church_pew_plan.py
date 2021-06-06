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
    
    gpdf_pew_seats = geopandas.GeoDataFrame(columns=['geometry'], data=pew_seats, crs='EPSG:27700')
    gpdf_pew_seats['pew_id'] = pew_id
    gpdf_pew_seats['seat_id'] = seat_id
    gpdf_pew_seats['neighs_left'] = neigh_left
    gpdf_pew_seats['neighs_right'] = neigh_right
        
    return gpdf_pews, gpdf_pew_seats
    

def create_extra_seats(pew_id_off=0, seat_id_off=0):
    # Behind Drum Cage
    tlx = 1500
    brx = 2000
    
    bry = 10000 + 800
    tly = bry + 500
    
    pews = list()
    pew_seats = list()
    pew_id = list()
    seat_id = list()
    neigh_left = list()
    neigh_right = list()
    first = True
    
    for i in range(6):
        poly = shapely.geometry.Polygon([(tlx, tly), (brx, tly), (brx, bry), (tlx, bry), (tlx, tly)])
        pews.append(poly)
        pew_seats.append(poly)
        
        bry = tly
        tly = bry + 500
        
        pew_id.append(1+pew_id_off)
        seat_id.append(i+1+seat_id_off)
        
        if first:
            neigh_left.append(0)
            first = False
        else:
            neigh_left.append(i+seat_id_off)
            
        if (i+1) == 6:
            neigh_right.append(0)
            first = False
        else:
            neigh_right.append(i+2+seat_id_off)
            
    # Add Chairs by Piano
    tlx = 18200 + 500
    brx = tlx + 500
    
    # Add chair #1
    bry = 10000 + 2000
    tly = bry + 500
    
    poly = shapely.geometry.Polygon([(tlx, tly), (brx, tly), (brx, bry), (tlx, bry), (tlx, tly)])
    pews.append(poly)
    pew_seats.append(poly)
    
    pew_id.append(2+pew_id_off)
    seat_id.append(7+seat_id_off)
    
    neigh_left.append(0)
    neigh_right.append(8+seat_id_off)
    
    
    # Add chair #2
    bry = tly
    tly = bry + 500
    
    poly = shapely.geometry.Polygon([(tlx, tly), (brx, tly), (brx, bry), (tlx, bry), (tlx, tly)])
    pews.append(poly)
    pew_seats.append(poly)
    
    pew_id.append(2+pew_id_off)
    seat_id.append(8+seat_id_off)
    
    neigh_left.append(7+seat_id_off)
    neigh_right.append(0)
    
    
    # Add chair #3
    bry = tly + 2000
    tly = bry + 500
    
    poly = shapely.geometry.Polygon([(tlx, tly), (brx, tly), (brx, bry), (tlx, bry), (tlx, tly)])
    pews.append(poly)
    pew_seats.append(poly)
    
    pew_id.append(3+pew_id_off)
    seat_id.append(9+seat_id_off)
    
    neigh_left.append(0)
    neigh_right.append(10+seat_id_off)
    
    
    # Add chair #4
    bry = tly
    tly = bry + 500
    
    poly = shapely.geometry.Polygon([(tlx, tly), (brx, tly), (brx, bry), (tlx, bry), (tlx, tly)])
    pews.append(poly)
    pew_seats.append(poly)
    
    pew_id.append(3+pew_id_off)
    seat_id.append(10+seat_id_off)
    
    neigh_left.append(9+seat_id_off)
    neigh_right.append(0)
    
    
    gpdf_pews = geopandas.GeoDataFrame(columns=['geometry'], data=pews, crs='EPSG:27700')
    gpdf_pews['pew_id'] = pew_id
    gpdf_pews['seat_id'] = seat_id
    gpdf_pews['neighs_left'] = neigh_left
    gpdf_pews['neighs_right'] = neigh_right
    
    gpdf_pew_seats = geopandas.GeoDataFrame(columns=['geometry'], data=pew_seats, crs='EPSG:27700')
    gpdf_pew_seats['pew_id'] = pew_id
    gpdf_pew_seats['seat_id'] = seat_id
    gpdf_pew_seats['neighs_left'] = neigh_left
    gpdf_pew_seats['neighs_right'] = neigh_right
    
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

pew_widths = [2000, 3000, 3000, 3000, 2000, 2000, 3000, 3000, 3000, 2000, 2000]
pew_x_off = [1000, 0, 0, 0, 1000, 1000, 0, 0, 0, 1000, 1000]
gpdf_pews_5, gpdf_pew_seats_5 = create_row(pew_widths, length=850, start_x=14300, start_y=10000, pew_x_off=pew_x_off, pew_id_off=pew_id_off, seat_id_off=seat_id_off)
pew_id_off = pew_id_off + gpdf_pews_5.pew_id.unique().shape[0]
seat_id_off = seat_id_off + gpdf_pews_5.shape[0]

pew_widths = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000]
gpdf_pews_6, gpdf_pew_seats_6 = create_row(pew_widths, length=850, start_x=18200, start_y=10000, pew_id_off=pew_id_off, seat_id_off=seat_id_off)
pew_id_off = pew_id_off + gpdf_pews_6.pew_id.unique().shape[0]
seat_id_off = seat_id_off + gpdf_pews_6.shape[0]

# Add extra seats behind drum cage and near piano.
gpdf_pews_7, gpdf_pew_seats_7 = create_extra_seats(pew_id_off=pew_id_off, seat_id_off=seat_id_off)



gpdf_pews = pandas.concat([gpdf_pews_1, gpdf_pews_2, gpdf_pews_3, gpdf_pews_4, gpdf_pews_5, gpdf_pews_6, gpdf_pews_7])
gpdf_pew_seats = pandas.concat([gpdf_pew_seats_1, gpdf_pew_seats_2, gpdf_pew_seats_3, gpdf_pew_seats_4, gpdf_pew_seats_5, gpdf_pew_seats_6, gpdf_pew_seats_7])

gpdf_pews.to_file('stmikes_pews_base.geojson', driver='GeoJSON')

gpdf_pew_seats.to_file('stmikes_seats_base.geojson', driver='GeoJSON')


