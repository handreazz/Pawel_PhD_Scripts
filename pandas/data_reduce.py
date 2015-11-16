import pandas as pd
import numpy as py

#~ trip = pd.read_csv('trip_data_3.csv')
#~ fare = pd.read_csv('trip_fare_3.csv')
#~ 
#~ trip_red = trip.ix[0:1000]
#~ fare_red = fare.ix[0:1000]
#~ 
#~ trip_red.to_csv('trip_data_3_reduced.csv')
#~ fare_red.to_csv('trip_fare_3_reduced.csv')


#~ trip = pd.read_csv('trip_data_3_reduced.csv')
#~ trip.drop([' passenger_count','medallion', ' dropoff_datetime',
#~ ' vendor_id', ' rate_code', ' store_and_fwd_flag'],1, inplace=True)
#~ print "saving trip"
#~ trip.to_csv('trip.csv')
#~ del trip
#~ print "trip done"
#~ 
#~ 
#~ fare = pd.read_csv('trip_fare_3_reduced.csv')
#~ fare.drop(['medallion',' vendor_id', ' pickup_datetime',
#~ ' surcharge', ' mta_tax', ' tolls_amount'],1, inplace=True)
#~ print "saving fare"
#~ fare.to_csv('fare.csv')
#~ del fare
#~ print "fare done"

print "reading trip"
trip = pd.read_csv('trip.csv')
print "reading fare"
fare = pd.read_csv('fare.csv')
print "merging"
trip = trip.merge(fare, on=' hack_license')
del fare
print "saving"
trip.to_csv('trip_data_fare.csv')
del trip
