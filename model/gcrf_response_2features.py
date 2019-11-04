import numpy as np
import sys
import global_var
from sgcrf import SparseGaussianCRF
from sklearn.metrics import mean_squared_error
sys.path.append(global_var.project_path+"/model")
import getSamples as gs
from preprocessing.fileprocessor import *
from preprocessing.preprocessor import *
from preprocessing.calculateError import *


historical_weeks = 1
predicted_weeks = 1
percentage = 0.75
x_length = historical_weeks*24
y_length = predicted_weeks*12
iterations = 10 #number of GCRF models
testSample = y_length/2
suitableError = .08
input_dim = 3 #number of features in the input: water, day of the week, hour of the day
n_iter = 1000
lr=0.01
data_path = global_var.current_data_path

rmse_day_path = global_var.project_path+"/Results/Hourly/gcrf/"



#top_buildings = ['BR','CE','DE','FA','C4','DG','EB','ES','GE','JS','LH','OO','PF','RA','RC','S1','S2','S3','SN','BN']

#correct = ['BN','BR','DG','EB','ES','GE','JS','S2','S3','SN','DE','FA','C4','LH','RA']
top = ['BN']# ['BN','BR','C4','DE','DG','EB','ES']
top_buildings = top
#top_buildings =['BN']

for building in top_buildings:

	lossIt = ["trainLoss"]
	train_RMSE = ["trainRMSE"]
	testing_RMSE = ["testRMSE"]
	train_RMSE_avg = ["trainRMSE-avg"] # it did not have title
	test_RMSE_avg = ["testRMSE-avg"]

	predicted_value_path = rmse_day_path + building + "_24_12_pred_L3_T5.txt"
	real_value_path = rmse_day_path + building + "_24_12_real_L3_T5.txt"
	rela_error_path = rmse_day_path + building + "_24_12_relativeError_L3_T5.txt"
	filename = data_path+building+'.csv'

	print("Running for:",building)

	pred = open(predicted_value_path, "w")
	real = open(real_value_path, "w")
	error = open(rela_error_path,"w")
	fh2 = open(rmse_day_path + building + '.txt', "w")

	if input_dim>1:
		_ ,X_train, Y_train, X_test, Y_test=getSamplesWithDayHour(filename, x_length, y_length,percentage)
		Y_train = Y_train[:,0::input_dim]
		Y_test = Y_test[:,0::input_dim]
	else:
		X_train, Y_train, X_test, Y_test = getData(filename, x_length, y_length,percentage) #gs.getSamples(filename, x_length, y_length)
		X_train = np.squeeze(X_train)
		Y_train = np.squeeze(Y_train)
		X_test = np.squeeze(X_test)
		Y_test = np.squeeze(Y_test)
	print X_train.shape, Y_train.shape, X_test.shape, Y_test.shape


	#response_times,
	model =  SparseGaussianCRF(lamL=0.8, lamT=0.5,learning_rate=lr, n_iter=n_iter)  #lamL and lamT are regularization parameters

	predictions = []
	#counter = 0;
	#run the model a few times and store predictions
	real_value = Y_test
	for k in range(1, len(Y_test)):
		for l in range(0, y_length):
			real.write(str(round(real_value[k][l], 2)) + ",")
		real.write("\n")
	X_test = np.array(X_test)
	Y_test = np.array(Y_test)
	X_train = np.array(X_train)
	Y_train = np.array(Y_train)
	counter = 0
	rmse1 = [i for i in range(y_length)]
	rmse2 = [i for i in range(y_length)]
	rmse3 = [i for i in range(y_length)]

	for i in range(0,iterations):
		#print("Iterations ",i,"\n")
		model.fit(X_train, Y_train)

		#saving the loss
		loss = model.lnll[-1]
		lossIt.append(loss)

		pred_train = model.predict(X_train)
		prediction = model.predict(X_test)

		terminate = 0
		predictions.append(prediction)

		rmse_train = RMSE(pred_train, Y_train)
		rmse_days = RMSE(prediction, Y_test)
		avgRMSE_train = np.mean(rmse_train)
		avgRMSE_test = np.mean(rmse_days)
		relerror0_train, relerror1_train, avg0_train, avg1_train = RelE(pred_train, Y_train, y_length)
		relerror0_test, relerror1_test, avg0_test, avg1_test = RelE(prediction, Y_test, y_length)

		train_RMSE_avg.append(avgRMSE_train)
		test_RMSE_avg.append(avgRMSE_test)


		print "Loss:", loss , "AVG train RMSE:", np.round(avgRMSE_train,2), "AVG test RMSE:", np.round(avgRMSE_test,2), "RelErrs (train-test)",avg0_train,avg0_test

		counter += 1


	#predictions = predictions[2]
	predictions = predictions[counter-1]
	for k in range(0, predictions.shape[0]):
		for l in range(0, y_length):
			if(predictions[k][l] < 0):
				predictions[k][l] = 0
			pred.write(str(round(predictions[k][l], 2)) + ",")
			#error.write(str(round(predictions[k][l]-Y_test[k][l],2))+",")
		pred.write("\n")
		#error.write("\n")


	#predictions = np.array(predictions)

	#average different GCRF's predictions
	#predictions = np.mean(predictions, axis=0)

	#Get RMSE over each day, and different rmse calculations
	rmse_days = RMSE(predictions,Y_test)
	#rmse_days = [np.sqrt(x) for x in rmse_days]
	relative_error0, relative_error1, avg0, avg1 = RelE(predictions, Y_test, y_length)

	for r in rmse_days:
		fh2.write(str(r) + '\n')
	error.write("RE0  , RE1  ,\n")
	for i in range(y_length):
		error.write(str(round(relative_error0[i], 2)) + " ," + str(round(relative_error1[i], 2)) + "\n")
	error.write("\naverage0 : " + str(round(avg0, 2)) + "\naverage1 : " + str(round(avg1, 2)))


	fh2.close()
	pred.close()
	real.close()
	error.close()

	writeColumns(os.path.join(save_path_name,name+"_Train_loss_rmse.csv"), zip(lossIt,train_RMSE_avg, test_RMSE_avg))
	writeColumns(os.path.join(save_path_name,name+"_Train_rmse_STEP.csv"),zip(train_RMSE)) # saving the train RMSE values for every 200th epoch

print model.lrs[0:5], model.lrs[-5:]