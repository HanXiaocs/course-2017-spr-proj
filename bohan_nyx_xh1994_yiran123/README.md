
# Evaluating Airbnb in Boston Area

Author: [Bohan Li](https://github.com/bohanli0403), [Ningyi Xue](https://github.com/Ginnyxue), [Han Xiao](https://github.com/HanXiaocs), [Yiran Pan](https://github.com/yiran123)

## Introduction
As one of the most famous online marketplaces and hospitality service websites, Airbnb becomes more and more popular among travelers all around the world. However, do travelers really know the Airbnb housing they choose to stay? Unlike looking for a traditional hotel on travel agency websites, customers usually need to spend more time on finding a safe and convenient house that matches their expectation because Airbnb let hosts provide all the information, which could lead to the lack of credibility. In addition, according to our own experience, we find that people tends to give high ratings to hotels/Airbnbs due to many reasons(ex. give random score; hosts are really nice so they don't want to give low score; don't want to receive low score from the hosts; not familiar with the neighbors). Under the influences of many factors, the original airbnb review may be biased. In our project, we decide to let the data talks. Besides the original Airbnb reviews given by customers, we also evaluate other factors that could affect the qualities of Airbnb housings in Boston Area. The goal of our project is to help potential Airbnb customers to choose the best Airbnb of they needs.

## Tools and Dataset

### Programming Languages
1. Python
2. MongoDB
3. D3.js
4. Leaflet js

### Data Sets
1. City of Boston crime incident July 2012 - August 2015
   
   https://data.cityofboston.gov/Public-Safety/Crime-Incident-Reports-July-2012-August-2015-Sourc/7cdf-6fgx
2. Active Food Establishment Licenses
   
   https://data.cityofboston.gov/Permitting/Active-Food-Establishment-Licenses/gb6y-34cq
3. Food Establishment Inspections
   
   https://data.cityofboston.gov/Health/Food-Establishment-Inspections/qndu-wx8w
4. Entertainment Licenses
   
   https://data.cityofboston.gov/Permitting/Entertainment-Licenses/qq8y-k3gp
5. Airbnb Boston
   
   http://insideairbnb.com/get-the-data.html
   
6. MBTA Bus Sthttp://insideairbnb.com/get-the-data.htmlops
   
   http://datamechanics.io/data/wuhaoyu_yiran123/MBTA_Bus_Stops.geojson

### Data Retrival
In our project, we mainly use coordinates to locate places and employ geopy/vincenty to calculate the distances between places in different datasets in order to obtain a statistic.

| Transformations | Original Dataset                 | New combination|
| -------------   |:---------------:                 | --------------:|
| 1               | Active food establishment licence, Crime Boston | Crime number around each food establishment(within 1 mile)|
| 2               | MBTA Bus Stop, Airbnb Rating(Original), Entertainment License|Entertainment & bustop number around each Airbnb|
| 3               | Active food establishment licence, Food Establishment Inspection |Cleanliness level of food establishments(Passrate of inspections)|
| 4               |Cleanliness level of food establishments, Crime number around each food establishment(within 1 mile),Entertainment & bustop number around each Airbnb|Correlation coefficient|
| 5               |correlation coefficient|Food establishment score system|
| 6               |Food establishment score system, Airbnb Rating| Airbnb surrounding food establishment score (Average)|
| 7               |Airbnb Rating, Crime Boston | Crime number around each Airbnb(within 1 mile)|
| 8               |Airbnb Rating, Entertainment & bustop number around each Airbnb, Airbnb surrounding food establishment score (Average), Crime number around each Airbnb(within 1 mile)|Airbnb Score System|
| 9               |Airbnb Score System|Score distribution(for visualization)|

# Algorithm

## Score system 

In this project, the original Airbnb reviews by customers only serve as a part of the evaluation. For each Airbnb housing, we also count and calculate safety level, surrounding dining options (safety and cleanliness), recreations, entertainments, transportations (bus stops). Then we normalize and weight all scores evenly to get the final rating of Airbnb housings under our standard. 

Normalization:

![equation](http://latex.codecogs.com/gif.latex?x_%7Bnew%7D%20%3D%20%5Cfrac%7Bx-%20x_%7Bmin%7D%7D%7Bx_%7Bmax%7D%20-%20x_%7Bmin%7D%7D)

finalScore = (reviews + safety + transportation + recreationAndDinning)/4

Here's the weighted score frequency bar graph:

![image](https://github.com/bohanli0403/course-2017-spr-proj/blob/master/bohan_nyx_xh1994_yiran123/img/bar.png)

## Correlation Coefficient
The defination of correlation coefficient:

![equation](http://latex.codecogs.com/gif.latex?corr%28x%2Cy%29%3D%20%5Cfrac%7Bcov%28x%2Cy%29%7D%7Bstd%28x%29%20%5Ccdot%20std%28y%29%7D)

In our project, we calculate correlation coefficients between many factors to see how they are related. Here is the distribution (Our first visualization) as well as the corresponding analysis.








