The following compressed file contains all the datasets generated till now
non_processed_daily ->  contains the file without being processed with outlier and empty value updated on daily basis
non_processed_hourly ->  contains the file without being processed with outlier and empty value updated on hourly basis
all_processed_daily ->  contains the file after being processed with outlier and all the zero value updated on daily basis (processed -> outlier greater than 2000 removed with median ,
                            all zero has been replaced with help of near by non-zero value in linear pattern, The daily data is calculated by summing up the processed hourly data )
all_processed_hourly ->  contains the file after being processed with outlier and all the zero value updated on hourly basis (processed -> outlier greater than 2000 removed with median ,
                            all zero has been replaced with help of near by non-zero value in linear pattern)
missing_processed_daily ->  contains the file after being processed with outlier and missing  value updated on daily basis  (processed -> outlier greater than 2000 removed with median ,
                            all missing has been replaced with help of near by present value in linear pattern, The daily data is calculated by summing up the processed hourly data )
missing_processed_hourly ->  contains the file after being processed with outlier and missing value updated on hourly basis  (processed -> outlier greater than 2000 removed with median ,
                            all missing has been replaced with help of near by present value in linear pattern)
Daily -> contains the file corresponding to current splitting definition from split.py on daily basis (processed -> outlier greater than 2000 removed with median ,
                            all missing has been replaced with help of near by present value in linear pattern, The daily data is calculated by summing up the processed hourly data )
Hourly -> contains the file corresponding to current splitting definition from split.py on hourly basis (processed -> outlier greater than 2000 removed with median ,
                            all missing has been replaced with help of near by present value in linear pattern) it also contains the day number (1->sunday, 2->monday,
			     3->tuesday,4->wednesday,5->thursday,6->friday,7->saturday), the hour count(data from 12 Am to 1 am is count 1, and so on )


As we are updating outlier and missing value only, in our current data-sets, we simply added the hourly processed data to get daily data
