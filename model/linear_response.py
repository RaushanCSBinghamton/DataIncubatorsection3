import numpy as np
import sys
import global_var
sys.path.append(global_var.project_path+"/model")
import getSamples as gs
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
from preprocessing.fileprocessor import *
from preprocessing.preprocessor import *
from preprocessing.calculateError import *
import datetime
import os
import sys

'''
def rmse(y_hat,y):
	#Method 1
	#Get RMSE over each day
	rmse_days = np.sqrt(mean_squared_error(y_hat, y, multioutput='raw_values'))
	#Get average RMSE
	rmse1 = sum(rmse_days)/len(rmse_days)
	rmse1 = round(rmse1,2)
	#Method 2
	#Get sum of squares per day
	sum_of_squares = sum((y_hat - y)**2)
	#sum over days, divide by (num_days * num_samples), take sqrt()
	rmse2 = np.sqrt(sum(sum_of_squares)/(y_hat.shape[1]*y_hat.shape[0]))
	rmse2 = round(rmse2,2)

	rmse_days = rmse_days.tolist()
	rmse_days = [round(x,2) for x in rmse_days]

	return rmse_days,rmse1,rmse2
'''
def linear_regression_model():

	try:
		top_buildings = [sys.argv[1]]

	except:
		top_buildings = ['BN', 'BR', 'DG', 'EB', 'ES', 'GE', 'JS', 'S2', 'S3', 'SN', 'DE', 'FA', 'C4', 'LH', 'RA']



	try:
		x_length = sys.argv[4]

	except:
		x_length = 24

	try:
		y_length = sys.argv[5]

	except:
		y_length = 12

	percentage = 0.75
	iterations = 10  # number of GCRF models


	data_path = global_var.current_data_path

	#rmse_day_path = dir_path

	#top_buildings = ['BR', 'CE', 'DE', 'FA', 'C4', 'DG', 'EB', 'ES', 'GE', 'JS', 'LH', 'OO', 'PF', 'RA', 'RC', 'S1', 'S2',
	 #                'S3', 'SN', 'BN']

	#correct = ['BN', 'BR', 'DG', 'EB', 'ES', 'GE', 'JS', 'S2', 'S3', 'SN', 'DE', 'FA', 'C4', 'LH', 'RA']


	for building in top_buildings:
		folder = datetime.datetime.now().strftime("%y-%m-%d_%H-%M")
		dir_path = global_var.project_path + "/Results/Hourly/linear/"+building+"/"

		try:
			os.mkdir(dir_path)
		except OSError:
			print()

		dir_path += folder + "/"

		try:
			os.mkdir(dir_path)
		except OSError:
			print()


		real_value_path = dir_path + building + "_"+str(x_length)+"_"+str(y_length)+"_real.txt"
		rela_error_path = dir_path + building + "_"+str(x_length)+"_"+str(y_length)+"_relativeError.txt"


		predicted_value_path = dir_path + building + "_" + str(x_length) + "_" + str(y_length) + "_pred.txt"

		filename = data_path + building + '.csv'
		print("Running for:", building)

		pred = open(predicted_value_path, "w")
		real = open(real_value_path, "w")
		error = open(rela_error_path, "w")
		fh2 = open(dir_path + building + "_"+str(x_length)+"_"+str(y_length)+".txt", "w")
		param_file = open(dir_path+"params_history.txt","w")
		param_file.write("Building : "+building+"\nxlength : "+str(x_length)+"\nyLength : "+str(y_length)+"\n\n")
		param_file.close()


		X_train, Y_train, X_test, Y_test = getData(filename, x_length, y_length,percentage)

		x = [i for i in range(0, x_length)]
		y = [i for i in range(x_length, x_length + y_length)]
		x_days = np.array(x)
		y_days = np.array(y)
		x_days = x_days.reshape((-1, 1))
		y_days = y_days.reshape((-1, 1))

		predictions = []

			# for each test sample, fit a straight line and calculate the MSE

		model = linear_model.LinearRegression()
		counter = 0
		for i in range(0, X_test.shape[0]):
			real_value = X_test[i, :].reshape((-1, 1))
			model.fit(x_days, X_test[i, :].reshape((-1, 1)))
			prediction = model.predict(y_days)
			for k in range(0,y_length):
				if prediction[k][0] < 0:
					prediction[k][0] = 0
				pred.write(str(round(prediction[k][0],2))+",")

			pred.write("\n")

			for k in range(0, y_length):
				real.write(str(round(real_value[k][0],2))+",")
			real.write("\n")
			counter+=1
			predictions.append(prediction)

		predictions = np.array(predictions).reshape((-1, y_length))
		#pred.write(str(predictions))


			# Get RMSE over each day, and different rmse calculations
			#rmse_days, rmse1, rmse2 = rmse(predictions, Y_test)
		rmse_days =  RMSE(predictions,Y_test)
		relative_error0, relative_error1, avg0,avg1 = RelE(predictions,Y_test,y_length)

		for r in rmse_days:
			fh2.write(str(r) + '\n')
		error.write("RE0  , RE1  ,\n")
		for i in range(y_length):
			error.write(str(round(relative_error0[i],2))+" ,"+str(round(relative_error1[i],2))+"\n")
		error.write("\naverage0 : "+str(round(avg0,2))+"\naverage1 : "+str(round(avg1,2)))
		fh2.close()
		pred.close()
		real.close()
		error.close()

linear_regression_model()