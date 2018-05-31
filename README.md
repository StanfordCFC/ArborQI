# Arbor QI 

in which alex lu messes around and tries to visualize things 

## Objectives
We're trying to visualize various forms of data from our health record to obtain a better sense of patient numbers week over week, services provided, and other features.  

## Current Struggles
* It's really annoying to get the data out of the csv's because idk how to use pandas very well
* I have no idea what some of the data means (the categorical variable fields are hard to interpret)
* The CSVs generated from the health record are often 1-n joins which are super annoying to process


## Current Progress
* I know how to pull data :O 
* CSV reading is mostly ready :O 
* `pandas` dataframe things are almost ready? May take significantly longer

## Interesting Findings
* The year 2011 is really hard to parse because there are periods of just straight up data entry from previous years, such that the total number of patients that year is greater than the total number of patients in like 2017. :/ 


## Todo 
* Determine a new report generating structure to make data extraction easy
* Determine the appropriate visualizations for the data that we choose 



## About the code 

### External Dependencies:
```
numpy
matplotlib
pandas
seaborn
```

My python notebooks are doing weird things so a lot of the code is built into the util files. Visualization will definitely be debugged and tuned in the notebooks though, when I get there. 