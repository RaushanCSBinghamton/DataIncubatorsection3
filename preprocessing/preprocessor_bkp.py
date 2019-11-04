import numpy as np

#-----------------------------------------
# helper functions for getData()
#-----------------------------------------

def openFile(filename):
    data = []
    with open(filename) as f:
        for line in f:
            words = line.split()
            data.append(words[0])
    return data


def sampleData(dataset,x_length,y_length):
    x_data_limit = len(dataset) - (x_length+y_length)
    X = []
    Y = []
    for i in range(x_data_limit):
        # for the inputs
        temp_x = []
        for j in range(x_length):
            temp_x.append(dataset[i+j])
        X.append(temp_x)
        # for the outputs
        temp_y = []
        for j in range(y_length):
            temp_y.append(dataset[i+x_length+j])
        Y.append(temp_y)
    return X,Y
        

    
#-----------------------------------------
# main method to obtain data
#-----------------------------------------

# obtains the datasets -> used for the RNN model
# filename : the string name for the file
# x_length : length of the input(timesteps of the past)
# y_length : length of output(timesteps into future)
# percentage : the percentage of data to use for training and testing
import pandas as pd
import numpy as np

def getSamplesWithDayHour(filename, x_length, y_length, train_percent, limitOutlier=5000):

    #take response data from all agencies
    df = pd.read_csv(filename, delimiter=',')# np.genfromtxt(filename, delimiter=',')

    median = df.loc[df['Water flow']<=limitOutlier, 'Water flow'].median()
    df.loc[df['Water flow'] > limitOutlier, 'Water flow'] = np.nan
    df.fillna(median,inplace=True)
    data = df[["Water flow","Day Number","Hour Number"]]


    days =  data["Water flow"] #[:,0]
    demands = data["Day Number"]#[1:,1]
    response_times = data["Hour Number"]#[1:,2]

    '''
        # This is done for 3d array for LSTM

        train_size = int(percentage*len(data))
        #test_size = int(len(data)-train_size)
        
        if input_dim == 1:
            train_data = np.array(data[1:train_size,None])
            test_data = np.array(data[train_size+1:-1, None])
        else:
            train_data = np.array(data[1:train_size])
            test_data = np.array(data[train_size+1:-1])
    '''

    num_train_rows = int(train_percent*len(days))    
    num_test_rows = len(days) - num_train_rows

    num_train_samples = num_train_rows-(x_length+y_length)-1 # to match exact numbers selected in 1 feature selection #+1
    num_test_samples = num_test_rows-(x_length+y_length)-1# to match exact numbers selected in 1 feature selection #+1
    #print("Number of training samples:",num_train_samples)
    #print("Number of testing samples:",num_test_samples)

    water_train_data = days[1:num_train_rows]
    water_test_data = days[num_train_rows:]

    print len(days), num_train_rows, num_test_samples, water_train_data.shape, water_test_data.shape

    response_train_data = response_times[1:num_train_rows] #dont look at last y_length data points for training
    response_test_data = response_times[num_train_rows:]#[-(num_test_rows):]
    demand_train_data = demands[1:num_train_rows]#[:num_train_rows]
    demand_test_data = demands[num_train_rows:]#[-(num_test_rows):]

    #construct train samples
    X_train_water = []
    Y_train_water = []

    X_train_response = []
    Y_train_response = []
    X_train_demand = []
    Y_train_demand = []

    #seperate samples for response and demand
    for i in range(0,num_train_samples): #num_train_samples
        xw = water_train_data[i:i+x_length] 
        yw = water_train_data[i+x_length:i+x_length+y_length]
        xr = response_train_data[i:i+x_length] #get all data for a particular train sequence
        yr = response_train_data[i+x_length:i+x_length+y_length] #get all labels for associated train sequence
        xd = demand_train_data[i:i+x_length]
        yd = demand_train_data[i+x_length:i+x_length+y_length]

        X_train_water.append(xw)
        Y_train_water.append(yw)
        X_train_response.append(xr)
        Y_train_response.append(yr)
        X_train_demand.append(xd)
        Y_train_demand.append(yd)

    X_train_water = np.array(X_train_water)
    Y_train_water = np.array(Y_train_water)
    X_train_response = np.array(X_train_response)
    X_train_demand = np.array(X_train_demand)
    Y_train_response = np.array(Y_train_response)
    Y_train_demand = np.array(Y_train_demand)

    print X_train_water.shape
    #X_train and Y_train are response and demand samples interwieved
    X_train = []
    Y_train = []

    for i in range(0,X_train_response.shape[0]):
        #print X_train_response[i,0],X_train_response[i,1], X_train_demand[i,0], X_train_demand[i,1]
        #ziping water, day, hour
        aux = np.hstack(zip(X_train_water[i,:],X_train_response[i,:],X_train_demand[i,:]))
        #zip pairs resp-demand and the stacks this horizontally: r1,d1,r2,d2 ....
        #print "aux shape ", aux.shape, aux[0:2],aux[0+14:2+14]
        X_interwieved = aux
        Y_interwieved = np.hstack(zip(Y_train_water[i,:],Y_train_response[i,:],Y_train_demand[i,:]))
        X_train.append(X_interwieved)
        Y_train.append(Y_interwieved)

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    #construct test sample
    X_test_water = []
    Y_test_water = []
    X_test_response = []
    Y_test_response = []
    X_test_demand = []
    Y_test_demand = []

    #seperate samples for response and demand
    for i in range(0, num_test_samples):
        xw = water_test_data[i:i+x_length] 
        yw = water_test_data[i+x_length:i+x_length+y_length]
        xr = response_test_data[i:i+x_length] #get all data for a particular train sequence
        yr = response_test_data[i+x_length:i+x_length+y_length] #get all labels for associated train sequence
        xd = demand_test_data[i:i+x_length]
        yd = demand_test_data[i+x_length:i+x_length+y_length]

        X_test_water.append(xw)
        Y_test_water.append(yw)
        X_test_response.append(xr)
        Y_test_response.append(yr)
        X_test_demand.append(xd)
        Y_test_demand.append(yd)

    X_test_water = np.array(X_test_water)
    Y_test_water = np.array(Y_test_water)
    X_test_response = np.array(X_test_response)
    X_test_demand = np.array(X_test_demand)
    Y_test_response = np.array(Y_test_response)
    Y_test_demand = np.array(Y_test_demand)

    print X_test_water.shape
    #X_test and Y_test are response and demand samples interwieved
    X_test = []
    Y_test = []
    for i in range(0,X_test_water.shape[0]):
        #print i
        X_interwieved = np.hstack(zip(X_test_water[i,:],X_test_response[i,:],X_test_demand[i,:]))
        Y_interwieved = np.hstack(zip(Y_test_water[i,:],Y_test_response[i,:],Y_test_demand[i,:]))
        X_test.append(X_interwieved)
        Y_test.append(Y_interwieved)

    X_test = np.array(X_test)
    Y_test = np.array(Y_test)

    return response_times, X_train, Y_train, X_test, Y_test

def stackHorizontally(dataset,input_dim=1):
    newSet = []
    for i in range(0,len(dataset)):
        instance = np.hstack(dataset[i])
        '''
        instance = dataset[i,0]
        for dim in range(1,input_dim):
            instance = zip(instance,dataset[i,dim]) #,X_test_response[i,:],X_test_demand[i,:]))
        instance = np.hstack(instance)
        '''
        newSet.append(instance)
    return np.array(newSet)

#75% - 25% in order
def getData(filename,x_length,y_length,percentage, input_dim=1, columns='C', typeModel=0,limitOutlier=5000):

    df = pd.read_csv(filename, delimiter=',')#,usecols=["Water flow"]
    #print df.columns
    median = df.loc[df['Water flow']<=limitOutlier, 'Water flow'].median()
    df.loc[df['Water flow'] > limitOutlier, 'Water flow'] = np.nan
    df.fillna(median,inplace=True)

    #Selecting columns for the dataset
    listCols = {'C':"Water flow",'D':"Day Number",'H':"Hour Number",'W':"Weekday"}
    listCols = [ listCols[column] for column in columns]

    print listCols
    data = df[listCols]
    '''
    if input_dim == 1:
        data = df["Water flow"]
    elif input_dim ==2:
        data = df[["Water flow","Day Number"]] #openFile(filename) # open the file and get data
    else: #if input_dim ==3:
        data = df[["Water flow","Day Number","Hour Number"]]
    '''
        #-- seperate training and testing --------
    train_size = int(percentage*len(data))
    #test_size = int(len(data)-train_size)
    
    train_data = np.array(data[1:train_size])
    test_data = np.array(data[train_size+1:-1]) #0 to get only the first column: consumption

    X_Train,Y_Train = sampleData(train_data,x_length,y_length)
    X_Test,Y_Test = sampleData(test_data,x_length,y_length)

    X_Train,Y_Train,X_Test,Y_Test = np.array(X_Train),np.array(Y_Train)[:,:,0],np.array(X_Test),np.array(Y_Test)[:,:,0]

    if typeModel==1:#LSTM needs it in 3D array and GCRF in 2D array

        X_Train = stackHorizontally(X_Train,input_dim)
        Y_Train = stackHorizontally(Y_Train,input_dim=1)
        X_Test = stackHorizontally(X_Test,input_dim)
        Y_Test = stackHorizontally(Y_Test,input_dim=1)

    print len(data), train_size, X_Train.shape, Y_Train.shape, X_Test.shape, Y_Test.shape

    return X_Train,Y_Train,X_Test,Y_Test


#getData('./../Data/processed_data/Hourly/BN.csv',24,12,0.75,input_dim=1, columns='C', typeModel=1,limitOutlier=5000)