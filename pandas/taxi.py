import pandas as pd
import numpy as np

trip = pd.read_csv('trip_data_3.csv')
trip.drop([' passenger_count','medallion',
' vendor_id', ' rate_code', ' store_and_fwd_flag'],1, inplace=True)
print "-> Trip data read successful"

fare = pd.read_csv('trip_fare_3.csv')
fare.drop(['medallion',' vendor_id', ' pickup_datetime',
' surcharge', ' mta_tax', ' tolls_amount'],1, inplace=True)
print "-> Trip fare read successful"

# verify 1 to 1 correspondence between the two data sets
#assert ( sum(trip.ix[:,'medallion'] == fare.ix[:,'medallion']) == trip.shape[0] )
#assert ( sum(trip.ix[:,' hack_license'] == fare.ix[:,' hack_license']) == trip.shape[0] )
#assert ( sum(trip.ix[:,' vendor_id'] == fare.ix[:,' vendor_id']) == trip.shape[0] )

d = trip.merge(fare, on=' hack_license')
del trip, fare
print "-> Data merge successful"

# Fix bad data points. NaN won't mess up pandas but 0's will skew means
# and such, so replace with NaN
d.loc[ d[' trip_time_in_secs'] == 0, [' trip_time_in_secs'] ] = np.nan
d.loc[ d[' fare_amount'      ] == 0, [' fare_amount'      ] ] = np.nan
d.loc[ d[' total_amount'     ] == 0, [' total_amount'     ] ] = np.nan
d.loc[ d[' trip_distance'    ] == 0, [' trip_distance'    ] ] = np.nan
d.loc[ d[' pickup_longitude' ] == 0, [' pickup_longitude' ] ] = np.nan    
d.loc[ d[' pickup_latitude'  ] == 0, [' pickup_latitude'  ] ] = np.nan    
d.loc[ d[' dropoff_longitude'] == 0, [' dropoff_longitude'] ] = np.nan    
d.loc[ d[' dropoff_latitude' ] == 0, [' dropoff_latitude' ] ] = np.nan 
print "-> Bad data points replaced.\n"


#Q1
ans = float (sum((d[' total_amount'] < 5.0) & (d[' payment_type'] == 'CRD')))\
      / sum((d[' total_amount'] < 5.0)) *100
print "Q1: %3.1f" %ans

#Q2
ans = (d[' fare_amount'] / d[' trip_time_in_secs'] * 60).mean()
print "Q2: %3.1f" %ans

#Q3
mph = d[' trip_distance'] / d[' trip_time_in_secs'] *60 *60
ans = mph.quantile(q=0.95)
print "Q3: %3.1f" %ans

#Q4
jfk = d[  ((d[' pickup_longitude'] > -73.8200) &
           (d[' pickup_longitude'] < -73.7700))&
          ((d[' pickup_latitude']  >  40.6350) &
           (d[' pickup_latitude']  <  40.6550))   ]
ans = jfk[' tip_amount'].mean()
print "Q4: %3.1f" %ans

#Q5
ans = float (sum((d[' total_amount'] > 50.0) & (d[' payment_type'] == 'CRD')))\
      / sum((d[' total_amount'] > 50.0)) *100
print "Q5: %3.1f" %ans

#Q6
ans = (d[' fare_amount']/d[' trip_distance']).median()
print "Q6: %3.1f" %ans

#Q7
# modified from http://www.johndcook.com/blog/python_longitude_latitude/
import math
def get_lat_long_distance(row):
    lat1 = row[' pickup_latitude']
    long1 = row[' pickup_longitude']
    lat2 = row[' dropoff_latitude']
    long2 = row[' dropoff_longitude']
    if np.nan in [lat1, long1, lat2, long2]:
      return np.nan
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    try:
      arc = math.acos( cos )
    except ValueError:
      # cos=1.0, pickup and dropoff are same location and distance is zero
      return 0.0
    miles = arc*3960
    return miles
dist_direct = d.apply(get_lat_long_distance, axis=1)
# there's a lot of bad data in the latitudes/longitudes. To be safe remove
# any data where the straight line distance is longer than the driving
# distance. Some of these points will have been "good" so the mean will 
# be very slightly down-shifted.
mask_distances = dist_direct<t[' trip_distance']
dist_direct = dist_direct[mask_distances]
t = t[mask_distances]
ans = (dist_direct / d[' trip_distance']).mean()
print "Q7: %3.1f" %ans

#Q8
d[' pickup_datetime'] = d[' pickup_datetime'].astype('datetime64[ns]')
month_mask = d[' pickup_datetime'].map(lambda x: x.month) == 3
driver_groups = d[[' hack_license', ' total_amount']][month_mask].groupby(' hack_license')
ans = driver_groups[' total_amount'].aggregate(np.sum).median()
print "Q8: %3.1f" %ans

