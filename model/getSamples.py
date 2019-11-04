import numpy as np
import sys

def getResponseAndDemand(filename):
	#filename = agency+'_Response_Demand.csv'
	data = np.genfromtxt(filename, delimiter=',')
	response_times = data[1:,2]
	demands = data[1:,1]
	return response_times, demands

#get response time sequence from particular agency
def getResponseTimes(agency, percent_train):
	filename = agency+'_Response_Demand.csv'
	data = np.genfromtxt(filename, delimiter=',')
	response_times = data[1:,3]
	train = response_times[:int(percent_train*len(response_times))]
	test = response_times[int(percent_train*len(response_times)):]
	return train, test

#use x_length number of historical time indicies (per agency)
#predict the final y_length number of time indicies (per agency)
def getSamplesWithDemand(filename, x_length, y_length):

	#take response data from all agencies
	data = np.genfromtxt(filename, delimiter=',')
	days = data[1:,0]
	demands = data[1:,1]
	response_times = data[1:,2]

	train_percent = 0.75

	num_train_rows = int(train_percent*len(days))
	num_test_rows = len(days) - num_train_rows

	num_train_samples = num_train_rows-(x_length+y_length)+1
	num_test_samples = num_test_rows-(x_length+y_length)+1
	#print("Number of training samples:",num_train_samples)
	#print("Number of testing samples:",num_test_samples)

	response_train_data = response_times[:num_train_rows] #dont look at last y_length data points for training
	response_test_data = response_times[-(num_test_rows):]
	demand_train_data = demands[:num_train_rows]
	demand_test_data = demands[-(num_test_rows):]

	#construct train samples
	X_train_response = []
	Y_train_response = []
	X_train_demand = []
	Y_train_demand = []

	#seperate samples for response and demand
	for i in range(0, num_train_samples):
		xr = response_train_data[i:i+x_length] #get all data for a particular train sequence
		yr = response_train_data[i+x_length:i+x_length+y_length] #get all labels for associated train sequence
		xd = demand_train_data[i:i+x_length]
		yd = demand_train_data[i+x_length:i+x_length+y_length]
		X_train_response.append(xr)
		Y_train_response.append(yr)
		X_train_demand.append(xd)
		Y_train_demand.append(yd)

	X_train_response = np.array(X_train_response)
	X_train_demand = np.array(X_train_demand)
	Y_train_response = np.array(Y_train_response)
	Y_train_demand = np.array(Y_train_demand)

	#X_train and Y_train are response and demand samples interwieved
	X_train = []
	Y_train = []
	for i in range(0,X_train_response.shape[0]):
		X_interwieved = np.hstack(zip(X_train_response[i,:],X_train_demand[i,:]))
		Y_interwieved = np.hstack(zip(Y_train_response[i,:],Y_train_demand[i,:]))
		X_train.append(X_interwieved)
		Y_train.append(Y_interwieved)

	X_train = np.array(X_train)
	Y_train = np.array(Y_train)

	#construct test sample
	X_test_response = []
	Y_test_response = []
	X_test_demand = []
	Y_test_demand = []

	#seperate samples for response and demand
	for i in range(0, num_test_samples):
		xr = response_test_data[i:i+x_length] #get all data for a particular train sequence
		yr = response_test_data[i+x_length:i+x_length+y_length] #get all labels for associated train sequence
		xd = demand_test_data[i:i+x_length]
		yd = demand_test_data[i+x_length:i+x_length+y_length]
		X_test_response.append(xr)
		Y_test_response.append(yr)
		X_test_demand.append(xd)
		Y_test_demand.append(yd)

	X_test_response = np.array(X_test_response)
	X_test_demand = np.array(X_test_demand)
	Y_test_response = np.array(Y_test_response)
	Y_test_demand = np.array(Y_test_demand)

	#X_test and Y_test are response and demand samples interwieved
	X_test = []
	Y_test = []
	for i in range(0,X_test_response.shape[0]):
		X_interwieved = np.hstack(zip(X_test_response[i,:],X_test_demand[i,:]))
		Y_interwieved = np.hstack(zip(Y_test_response[i,:],Y_test_demand[i,:]))
		X_test.append(X_interwieved)
		Y_test.append(Y_interwieved)

	X_test = np.array(X_test)
	Y_test = np.array(Y_test)

	#get last test sample to predict individual sample
	#X_test_last = X_test[-1,:]
	#Y_test_last = Y_test[-1,:]

	return response_times, X_train, Y_train, X_test, Y_test

#dont consider demand
def getSamples(filename, x_length, y_length):

	#take response data from all agencies
	#chosen_agency = agency
	#filename = chosen_agency+'_Response_Demand.csv'
	data = np.genfromtxt(filename, delimiter=',')
	days = data[1:,0]
	response_times = data[1:,2] #ignore header and id column

	train_percent = 0.75

	num_train_rows = int(train_percent*len(days))
	num_test_rows = len(days) - num_train_rows

	num_train_samples = num_train_rows-(x_length+y_length)+1
	num_test_samples = num_test_rows-(x_length+y_length)+1
	#print("Number of training samples:",num_train_samples)
	#print("Number of testing samples:",num_test_samples)

	train_data = response_times[:num_train_rows] #dont look at last y_length data points for training
	test_data = response_times[-(num_test_rows):]
	#construct train samples
	X_train = []
	Y_train = []
	for i in range(0, num_train_samples):
		x = train_data[i:i+x_length] #get all data for a particular train sequence
		y = train_data[i+x_length:i+x_length+y_length] #get all labels for associated train sequence
		X_train.append(x)
		Y_train.append(y)

	#construct test sample
	X_test = []
	Y_test = []	
	for i in range(0, num_test_samples):
		x = test_data[i:i+x_length] #get all data for a particular train sequence
		y = test_data[i+x_length:i+x_length+y_length] #get all labels for associated train sequence
		X_test.append(x)
		Y_test.append(y)

	X_train = np.array(X_train)
	Y_train = np.array(Y_train)
	X_test = np.array(X_test)
	Y_test = np.array(Y_test)

	#get last test sample to predict individual sample
	#X_test_last = test_data[-(x_length+y_length):-(y_length)]
	#Y_test_last = test_data[-(y_length):]

	return response_times, X_train, Y_train, X_test, Y_test