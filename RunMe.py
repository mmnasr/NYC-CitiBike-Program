# Data Incubator Challenge Question: 
# By: Mohamad Nasr-Azadani. mmnasr@gmail.com
# NYC Citi-bike program.

import pandas as pd
import numpy as np

def main():
    df = load_and_prepare_data(load_prepared_data=False, add_arcdistance_column=True, save_data=True)
    part1_median_trip_duration(df)
    part2_fraction_of_rides_same_start_stop(df)
    part3_standard_deviation_bike_station_visit(df)
    part4_average_trip_length(df)    
    part5_average_duration_of_trips_monthly(df)    
    part6_largest_ratio_of_hourly_usage(df)    
    part7_fraction_of_rides_exceeding_time_limit(df)    
    part8_average_number_of_time_bike_moved(df)    

#**********************************************************************************************************
# This function computes the 'great circle arc' distance given 
# the coordinates of (latitude, longitude) the start and end stations 
def comput_trip_length(df):
    R = 6371 # Earth radius

    darc = pd.np.deg2rad(df['start station latitude']).to_frame('lat1')
    darc['lat2'] = pd.np.deg2rad(df['end station latitude'])
    darc['long1'] = pd.np.deg2rad(df['start station longitude'])
    darc['long2'] = pd.np.deg2rad(df['end station longitude'])
    darc['sin_phi'] = pd.np.sin(0.5*(darc['lat2'] - darc['lat1']))
    darc['sin_landa'] = pd.np.sin(0.5*(darc['long2'] - darc['long1']))#.to_frame('sin_landa')
    darc['a_term'] = darc['sin_phi']*darc['sin_phi'] + darc['sin_landa']*darc['sin_landa'] * np.cos(darc['lat1'])*np.cos(darc['lat2'])
    darc['arcdistance'] = R*(2.0*np.arctan2(np.sqrt( darc['a_term']), np.sqrt( 1.0-darc['a_term'])))
    
    return darc['arcdistance']

def load_and_prepare_data(load_prepared_data=False, add_arcdistance_column=True, save_data=True):

    if (load_prepared_data):
        print("Loading 2015-prepared_data.csv ...")
        df = pd.read_csv("2015-prepared_data.csv", parse_dates=['starttime', 'stoptime'] )
        print("successfully.")
        return df
    # else

    # Go through monthly zipped csv files and import them as dataframe. 
    # Append all those files to a massive dataframe
    n_months = 12
    for month in range(1,n_months+1):
        filename = "2015"+str(month).zfill(2)+"-citibike-tripdata.zip"
        print("Loading: "+filename)
        dm = pd.read_csv(filename, parse_dates=['starttime', 'stoptime'])
        if (month == 1):
            df = dm
        else:
            df = pd.concat([df, dm])
    
    # To save memory, we compute the trip lenght at this stage. 
    # Upon completing this, we can eliminate four columns (latitude and longitute of start and end stations)
    # from the original dataframe
    if (add_arcdistance_column):
        # Add a new column to original dataframe
        df['trip length'] = comput_trip_length(df)
        print('\nTrip length calcualted based on "great arc circle". New column added as "trip length".')

    # Drop columns that are not necessary for the rest of this Challenge. 
    delete_cols = ['start station name', 'start station latitude', 'start station longitude', 'end station name', 'end station latitude', 'end station longitude', 'birth year', 'gender']
    print('\nUnnecessary columns dropped:')
    print(delete_cols)
    df.drop(delete_cols, axis=1, inplace=True)

    if (save_data):
        fnameout = "2015-prepared_data.csv"
        df.to_csv(fnameout, index=False)
        print('\nData saved to ' + fnameout)
        
    return df

# *****************************************************************************************
# *****************************************************************************************
# *****************************************************************************************
# Part 1: What is the median trip duration, in seconds?
def part1_median_trip_duration(df):
    print("Part1: Median trip duration in 2015 was: " + str(df['tripduration'].median()) + ' seconds')
    
    
# Part 2: What fraction of rides start and end at the same station?
def part2_fraction_of_rides_same_start_stop(df):
    Nt = len(df)
    N_same_stations = len(df[df['start station id'] == df['end station id']])
    print('Part 2: Fraction of rides start and end at the same station:' + str(N_same_stations/float(Nt)))    

# What is the standard deviation of the number of stations visited by a bike?
def part3_standard_deviation_bike_station_visit(df):
    # First, group dataset by bikeid
    grouped = df.groupby('bikeid',as_index=False)['start station id', 'end station id']

    # Now go through each group, create a set of both start and end stations, drop the duplicates and find the length. 
    # This should give the number of stations visited by a unique bike
    bike_station_visit_count = {}
    for bikeid, group in grouped:
        bike_station_visit_count[bikeid] = len(pd.unique(group[['start station id', 'end station id']].values.ravel()))

    visits = bike_station_visit_count.values()
    standard_dev = np.std(visits)
    
    print("Part 3: Standard deviation of the number of stations visited by a bike: " + str(standard_dev))    

# Part 4: What is the average length, in kilometers, of a trip? 
def part4_average_trip_length(df):
    dtemp = df[df['trip length'] > 0]
    print('Part 4: Average length, in kilometers, of a trip (excluding trips with the same start and stop stations): ' + str(dtemp['trip length'].mean()))    
    
def part5_average_duration_of_trips_monthly(df):
    df['startmonth'] = df['starttime'].dt.month
    monthly_tripduration_average = df.groupby('startmonth')['tripduration'].mean()
    print('Part 5: Difference between maximum and minimum average of monthly trip durations: '+ str(max(monthly_tripduration_average) - min(monthly_tripduration_average)) + ' second.')
    
# What is the largest ratio of station hourly usage fraction to system hourly usage fraction (hence corresponding to the most "surprising" station-hour pair)?
def part6_largest_ratio_of_hourly_usage(df):
    # Extract hour and add it as a new column
    df['hour'] = df['starttime'].dt.hour

    # Group by 'start station id'. Then get the size to return the total number of trips started at each station in 2015
    stations_total_trip_count_2015 = df.groupby(['start station id']).size()

    # hours: 0,1,...,23
    hourly_trip_fraction_whole_system = df.groupby('hour').size() / float(len(df))

    # hours: 0,1,...,23
    # start station id: (many values)
    # number of trips took place during that hour for each station
    hourly_trip_count_each_station = df.groupby(['hour', 'start station id']).size()

    max_ratio = 0.0
    for hr_stid, trip_count in hourly_trip_count_each_station.iteritems():
        # hour
        hr = hr_stid[0]
        # start station id 
        station_id = hr_stid[1]

        # Total number of trips from 'start station id' in 2015
        total_count_station = stations_total_trip_count_2015[station_id]

        # Hourly fraction of trips from 'start station id' occuring at current hour (to the whole trips in 2015 for current station)
        st_fraction = trip_count / float(total_count_station)

        # Hourly fraction of trips from all stations occuring at current hour (to the whole trip count in 2015)
        wh_fraction = hourly_trip_fraction_whole_system[hr]
        max_ratio = max(max_ratio, (st_fraction/wh_fraction))
    
    print("Part 6: Largest ratio of station hourly usage fraction to system hourly usage fraction: " + str(max_ratio)) 

    
# What fraction of rides exceed their corresponding time limit?
def part7_fraction_of_rides_exceeding_time_limit(df):
    Nt = len(df)
    # Regular customers exceeding their allowed time
    allowed_time = 30*60 # Regular customers (seconds)
    N_customer_exceed = len(df[(df['usertype'] == 'Customer') & (df['tripduration'] > allowed_time)])
    
    # Subscribed customers exceeding their allowed time
    allowed_time = 45*60 # Subscribed customers (seconds)
    N_subscriber_exceed = len(df[(df['usertype'] == 'Subscriber') & (df['tripduration'] > allowed_time)])    
    
    Fraction = (N_customer_exceed + N_subscriber_exceed)/float(Nt)
    print('Part 7: Fraction of rides exceed their corresponding time limit: ' + str(Fraction))
    
# What is the average number of times a bike is moved 
def part8_average_number_of_time_bike_moved(df):

    # Sort by bikeid first, then sort by trip starttime
    df.sort_values(by=['bikeid', 'starttime'], ascending=[True, True], inplace=True)

    # Now with the soted dataframe, for each bike we like to find out the previous end station id. 
    # Shift the entire rows of 'end station id' one below and copy the results as a new column defining 
    # 'previous trip end station id'
    df['previous trip end station id'] = df['end station id'].shift()

    # Replace the NaN values by the value of the 'start station id'. 
    # Note that we alway gets one on the first row since we shift the rows down by one.
    df['previous trip end station id'].fillna(df['start station id'], inplace=True)

    # Convert float to int
    df['previous trip end station id'] = df['previous trip end station id'].astype(int)
    
    # Now, for each bike, check the two columns 'start station id' and 'previous trip end station id'. 
    # If they are not the same, them the bike is moved for maintenance or re-distribution.
    df['moved'] = (df['previous trip end station id'] != df['start station id'])

    # Number of times each bike is moved from previously parked station
    # groupy dataset by bikeid. Sum (1:True) and it will give us the total number of time each bike is moved. 
    bike_moved_count = df.groupby('bikeid')['moved'].sum()
    print("Part 8: The average number of times a bike is moved for redistribution or maintenance: " + str(bike_moved_count.mean()))


main()

