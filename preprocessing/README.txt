Split.py Description
    Hourly data:
        First all the data is collected from 3rd July to 28 December 2018. The missing value is replaced with -1, so that it can be replaced later. The collection is done for each building.
        Then each value is rounded of to two decimal value and the missing data is replaced in linear pattern (eg-> if data is 1,0,0,0,5, the is replaced as 1,2,3,4,5)
        Later we have divided the building into 4 category.
            category 1 -> no edit needed
            category 2 -> trim data from 124 days to last
            category 3 -> trim last 1 week
            category 4 -> trim 1st 47 days
        based on this division we processed the data (some of building were included in both category 3 and 4)
        write the hourly processed data to the file
    Daily data
        Summing the processed hourly data gives the daily data
        write the daily processed data to the file