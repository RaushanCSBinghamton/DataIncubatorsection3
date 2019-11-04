"""
How I am filtering:

- Remove rows that dont have valid close date
- Remove rows that responded to by a top 8 agency
- Remove rows that has a complaint type differing from the list
- Remove rows that dont have 1 of the 5 major boroughs listed
- Remove rows before 2015
- Remove rows that have negative response times

### currently not touching outliers
- Change outliers to the median (an oulier is +-(8*median), or < 0)

The files produced has the median response times in hours, corresponding to the day

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import sys
from datetime import datetime
import statistics as stat
from datetime import date
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import global_var

#return a generator, so we dont have to load the whole file in memory
def read_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            yield row

#2012 and 2016 are leap years
def getDayNumber(year, month, day):
	year = year-2010 #2010 is the first year we have data for
	days_in_months = [31,28,31,30,31,30,31,31,30,31,30,31]
	day_num = (year*365)
	if((year > 2) or ((year == 2) and (month > 2))): #2012 leap year
		day_num += 1
	if((year > 6) or ((year == 6) and (month > 2))): #2016 leap year
		day_num += 1
	for i in list(range(0,month-1)):
		day_num += days_in_months[i]
	day_num += day
	return(day_num)

def subtractDates(start,end):
	format = '%m/%d/%Y %I:%M:%S %p'
	start_date = datetime.strptime(start, format)
	end_date = datetime.strptime(end, format)
	difference = (end_date-start_date).total_seconds()
	return int(difference)

def writeDatastructureToCSV(data_path, stats_path, data_structure_response, data_structure_demand, suggested_demand,building_day,building_hour,building_weekday):

	fh = open(stats_path,"w") #write statistics here

	for outer_key in data_structure_response.keys():
		if isinstance(outer_key, int):
			outer_key = str(outer_key)
		fh.write(outer_key+'\n')

		response_times = []
		demands = []
		day = []
		hour = []
		weekday = []
		for day_num in sorted(data_structure_response[outer_key].keys()):
			try:
				response_times.append(data_structure_response[outer_key][day_num][0])
				demands.append(data_structure_demand[outer_key][day_num])
				day.append(building_day[outer_key][day_num])
				if building_hour != '':
					hour.append(building_hour[outer_key][day_num])
				weekday.append(building_weekday[outer_key][day_num])
			except:
				print(str(day_num))

		median_response = stat.median(response_times)


		fh.write("Number of total data points: " + str(sum(demands)) + '\n\n')
		fh.write("Median water flow: "+str(median_response)+'\n')



		#change outliers in response and demand to the median
		median_demand = stat.median(demands)
		num_response_outliers = 0
		num_demand_outliers = 0

		fh.write("Response outliers: "+str(num_response_outliers)+'\n')
		fh.write("Demand outliers: "+str(num_demand_outliers)+'\n\n')

		#data = pd.DataFrame({'Response_Time':response_times, 'Demand':demands})
		if building_hour == '':
			data = pd.DataFrame(
				{'Water flow': response_times, 'data points': demands,
				 'Weekday': day})
			columnsTitles = ["data points", "Water flow", "Weekday"]
		else:
			data = pd.DataFrame({'Water flow': response_times,'data points':demands,'Day Number':day,'Hour Number':hour,'Weekday':weekday})
			columnsTitles = ["data points", "Water flow","Day Number","Hour Number","Weekday"]
		data = data.reindex(columns=columnsTitles)
		#replace any /'s in complaint with _, so the path isn't confused
		outer_key = outer_key.replace('/','_')

		data.to_csv(data_path+outer_key + '.csv')

	fh.close()


def sliceList(build,start,end,building_response):
	myList = {}
	for i in range(start,end) :
		try:
			myList[i-start]=building_response[build][i]
		except:
			print(build+"  -   "+str(i)+"  start "+str(start)+"  end  "+str(end))
	return myList

def split():

	start_day = 0
	if global_var.preprocessing_switch == 1:
		total_num_days = 170*24
		total_num_days_daily = 170
	else:
		total_num_days = 130 * 24
		total_num_days_daily = 130



	top_buildings = ['BN','BR','CE','DE','FA','C4','DG','EB','ES','GE','JS','LH','OO','PF','RA','RC','S1','S2','S3','SN']
	building_response = {building:{x:[] for x in range(start_day,total_num_days+1)} for building in top_buildings}
	building_demand = {building:{x:0 for x in range(start_day,total_num_days+1)} for building in top_buildings}
	building_nan ={building:0 for building in top_buildings}
	building_zero = {building:0 for building in top_buildings}
	building_missing_data = {building:0 for building in top_buildings}
	building_daily_response = {building:{x:[] for x in range(start_day,total_num_days_daily+1)} for building in top_buildings}
	building_day_daily = {building:{x:((x+3)%7)+1 for x in range(start_day,total_num_days_daily+1)} for building in top_buildings}
	building_day = {building:{x:((x+3)%7)+1 for x in range(start_day,total_num_days+1)} for building in top_buildings}
	building_hour = {building: {x: (x % 24) + 1 for x in range(start_day, total_num_days + 1)} for building in
					top_buildings}
	building_weekday = {building: {x: ((x + 3) % 7) + 1 for x in range(start_day, total_num_days + 1)} for building in
					top_buildings}

	for building in top_buildings:
		counter = 0
		for i in range(total_num_days+1):
			if i%24 ==0:
				counter+=1
			building_day[building][i] = ((counter+2)%7)+1
			if building_day[building][i] ==7 or building_day[building][i] ==1:
				building_weekday[building][i] = 0
			else:
				building_weekday[building][i] = 1


	file_generator = pd.read_csv(global_var.project_path +'/Data/Energy_water1.csv')


	start_time = file_generator['START_TIME'].tolist()
	building_id = file_generator['BUILDING_ID'].tolist()
	value = file_generator['VALUE'].tolist()

	for build in top_buildings:
		for line in range(start_day,total_num_days+1):
			building_response[build][line] = []
			building_demand[build][line] = 0
		for line in range(start_day,total_num_days_daily+1):
			building_daily_response[build][line] = []

	print("Finding Response Times...")

	#Search through all data points
	counter = 0


	list1 = ['S2','S3','SN','C4','GE'] # no trimming needed
	list2 = ['ES'] # trim from 124 days
	list3 = ['FA','LH','BN','BR','DE','JS','RA','DG'] # trim last 1 week
	list4 = ['BN','BR','DE','JS','RA','DG'] # trim 1st 47 days

	#for line in file_generator:
	for iterator in range(0,len(value)):
		counter = counter + 1
		if(counter > 4):

			#extract relevant info from data point
			created_date = start_time[iterator]

			year = int(created_date.split()[0].split('/')[2])
			month = int(created_date.split()[0].split('/')[0])
			day = int(created_date.split()[0].split('/')[1])
			Hr = int(created_date.split()[1].split(':')[0])
			if(created_date.split()[2] == 'PM' and Hr != 12):
				Hr = Hr + 12
			elif (created_date.split()[2] == 'AM' and Hr == 12):
				Hr = 0

			numDaysLimit = 170*24
			if global_var.preprocessing_switch == 1:
				d1 = date(2018, 7, 3)
			else:
				d1 = date(2018, 8, 1)
				numDaysLimit = 130*24
			d2 = date(year, month, day)
			numDays = abs(d2 - d1).days

			'''if(closed_date != '' and
				agency in top_agencies and
				complaint_type in complaints_list and
				borough in boroughs and
				year >= 2015):
	'''
			numDays = numDays * 24 + Hr

			if numDays >=0 and numDays <=numDaysLimit:

			#Check if data is valid
				if np.isnan(value[iterator]):
					building_response[building_id[iterator]][numDays].append(-1)
					building_nan[building_id[iterator]] = building_nan[building_id[iterator]] +1
				else :
					building_response[building_id[iterator]][numDays].append(value[iterator])
					building_demand[building_id[iterator]][numDays] = building_demand[building_id[iterator]][numDays] +1
					if value[iterator] == 0:
						building_zero[building_id[iterator]] = building_zero[building_id[iterator]] +1


	#now replace each response time list with its median value
	print("Finding missing data per hour...")

	for building in top_buildings:
		for i in range(start_day,total_num_days+1):
			sumValue = -1
			if(len(building_response[building][i]) > 0):
				sumValue = sum(building_response[building][i])

			building_response[building][i] = []
			#building_demand[building][i] = []
			if np.isnan(sumValue) :
				sumValue = -1
			building_response[building][i].append(round(sumValue,2))

	'''
	# analysis of zero data , missing data
	building_zero_nan = []
	building_zero_nan.append(["Building","ZERO COUNT", "NAN COUNT","MISSING VALUE", "Total Data"])
	for building in top_buildings:
		building_zero_nan.append([building,building_zero[building],building_nan[building],(building_missing_data[building]-building_zero[building]-building_nan[building]),total_num_days])
	file_path = global_var.project_path+'/Data/Binghamton_water/Hourly_data_analysis.csv'
	with open(file_path, 'a') as outcsv:
    	#configure writer to write standard csv file
    	writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

    	for item in building_zero_nan:
        	#Write item to outcsv
        	writer.writerow([item[0], item[1], item[2],item[3],item[4]])
	'''


	# replacing missing data
	for building in top_buildings:
		preIndex = 0
		zerolength = 0
		postIndex = 0
		flat_list = []
		counter =0
		for sublist in building_response[building]:
			for item in building_response[building][sublist]:
				flat_list.append(item)
		medianValue =  stat.mean(flat_list)

		for i in range(start_day,total_num_days+1):
			if building_response[building][i][0] > 2000:
				building_response[building][i][0] = medianValue
			if sum(building_response[building][i]) == -1:
				zerolength +=1
			else:
				if zerolength == 0:
					preIndex = i
				else:
					postIndex = i
					zerolength += 1
					for j in range(preIndex,postIndex):
						if preIndex == 0:
							building_response[building][j][0] =  ((j +1) * (
									building_response[building][postIndex][0]) / zerolength)
						else:
							building_response[building][j][0] = building_response[building][preIndex][0] + ((j-preIndex)*(building_response[building][postIndex][0]- building_response[building][preIndex][0])/zerolength)
						building_response[building][j][0] = round(building_response[building][j][0], 2)
					zerolength = 0
					preIndex = i
			building_response[building][i][0] = round(building_response[building][i][0],2)
		if zerolength > 0:
			for j in range(preIndex,total_num_days+1):
				building_response[building][j][0] = building_response[building][preIndex][0] - ((j-preIndex)*(building_response[building][preIndex][0])/zerolength)



	if global_var.preprocessing_switch == 1:
		for building in top_buildings:
			if building in list1:
				building_response[building] = sliceList(building, 8, len(building_response[building]),building_response)
			if building in list2:
				building_response[building] = sliceList(building,0,122*24-8,building_response)#building_response[building][:122*24-8]
			if building in list3:
				building_response[building] = sliceList(building,0,163*24,building_response)#building_response[building][:163*24]
			if building in list4:
				start = (47*24-8)
				building_response[building] = sliceList(building,start,len(building_response[building]),building_response)#building_response[building][47*24-8:]


	for building in top_buildings:
		my_list = [ [k,v] for k, v in building_response[building].items() ]
		my_list = my_list[:2632]+my_list[2800:]
		#plt.plot(my_list, label='Real')
		#plt.legend()
		#plt.show()
		building_response[building] = dict(my_list)

	building_data_path = global_var.project_path+'/Data/processed_data/Hourly/'
	building_stats_path = global_var.project_path+'/Data/stats/building_hourly.txt'
	writeDatastructureToCSV(building_data_path, building_stats_path, building_response,
		building_demand, '',building_day,building_hour,building_weekday)

	dayDict = {'BN':116,'BR':116,'CE':170,'DE':116,'FA':163,'C4':170,'DG':116,'EB':170,'ES':122,'GE':170,'JS':116,'LH':163,
		   'OO':170,'PF':170,'RA':116,'RC':170,'S1':170,'S2':170,'S3':170,'SN':170}
# converting hourly data to daily
	for building in top_buildings:
		sumValue = 0
		dailyCounter = 0
		counter = 0
		if global_var.preprocessing_switch == 1:
			endDay = dayDict[building]*24
			if building in list1 or building in list2:
				endDay -= 8
		else:
			endDay = 130*24
			list4 = []
		for i in range(start_day,endDay):
			try:
				sumValue+=building_response[building][i][0]

				counter+=1

				if counter == 24:
					building_daily_response[building][dailyCounter].append(sumValue)
					building_demand[building][dailyCounter] = 24
					sumValue = 0
					dailyCounter += 1
					counter = 0
			except:
				print("problem")
		if global_var.preprocessing_switch == 1:
			endDay = dayDict[building]
		else:
			endDay = 123
		for i in range(dailyCounter,endDay):
			building_daily_response[building][i].append(sumValue)
			building_demand[building][i] = counter
			sumValue = 0
			counter = 0




	total_num_days = total_num_days_daily

	building_data_path = global_var.project_path+'/Data/processed_data/Daily/'
	building_stats_path = global_var.project_path+'/Data/stats/building_daily.txt'
	writeDatastructureToCSV(building_data_path, building_stats_path, building_daily_response,
		building_demand, '',building_day_daily,'',building_weekday)
		

split()
