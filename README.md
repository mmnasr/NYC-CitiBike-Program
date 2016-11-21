# NYC-CitiBike-Program
## The Data Incubator Challenge Questions: The Citi Bike Program in New York City.

### The Citi Bike Program (https://www.citibikenyc.com/) is a bike sharing system in New York City. Cyclists can rent a bicycle from one of many stations around the city and return it to any other station. Citi Bike has released ridership information to the public. This contains a list of all rides taken, their start and end locations, their start and end times, and limited demographic information about the rider. We will be considering the data from 2015 only.

Q1: What is the median trip duration, in seconds?

Q2: What fraction of rides start and end at the same station?

Q3: We say a bike has visited a station if it has a ride that either started or ended at that station. Some bikes have visited many 
stations; others just a few. What is the standard deviation of the number of stations visited by a bike?

Q4: What is the average length, in kilometers, of a trip? Assume trips follow [great circle arcs](https://en.wikipedia.org/wiki/Great_circle) 
from the start station to the end station. Ignore trips that start and end at the same station, as well as those with obviously wrong data.

Q5: Calculate the average duration of trips for each month in the year. (Consider a trip to occur in the month in which it starts.) 
What is the difference, in seconds, between the longest and shortest average durations?

Q6: Let us define the hourly usage fraction of a station to be the fraction of all rides starting at that station that leave during a
specific hour. A station has surprising usage patterns if it has an hourly usage fraction for an hour significantly different from
the corresponding hourly usage fraction of the system as a whole. What is the largest ratio of station hourly usage fraction to
system hourly usage fraction (hence corresponding to the most "surprising" station hour pair)?


Q7: There are two types of riders: "Customers" and "Subscribers." (https://www.citibikenyc.com/pricing) Customers buy a short-time 
pass which allows 30-minute rides. Subscribers buy yearly passes that allow 45-minute rides. What fraction of rides exceed their corresponding time limit?


Q8: Most of the time, a bike will begin a trip at the same station where its previous trip ended. Sometimes a bike will be moved by the
program, either for maintenance or to rebalance the distribution of bikes. What is the average number of times a bike is moved
during this period, as detected by seeing if it starts at a different station than where the previous ride ended?

### Requirements: 
python, pandas, numpy

### Solution:
Can be found here: [solution](RunMe.ipynb)
