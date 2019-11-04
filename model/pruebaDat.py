
from preprocessing.fileprocessor import *
from preprocessing.preprocessor import *
from preprocessing.calculateError import *

X_train_data, Y_train_data, X_test_data, Y_test_data = getData('./../Data/processed_data/Hourly/BN.csv',24,12,0.75,0)