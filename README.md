- Overlapped slide windows with stride 1, also mentioned in the paper
- Training in al the 75% of the dataset and then training 10% of it (for generalization?)
- Seems like randomized training is not worth it:

49900  loss : 51.092957  output size : (10, 2969, 1)
-- training stopped @ epoch : 50000
--- randomized training started ---
50000  loss : 60.66044  output size : (10, 297, 1)

- For that I would say to batch the 75%, average in each epoch and then compare it to the 10%. Is it really working? See the convergence of LOSS in time
- Try regularization or not
- Is the MSE the loss function?
- ? Curriculum learning is the same as scheduling learning that they say did not work as well as only taking predicted previous
- found is on test
- ?  unlike machine translation that uses a flagged value for the initialization, we use the final signal strength. Does it refer to the <go> tag?
- ? Did we arrive to the limit MSE<9 or RMSE<? or just got the EPOCH LIMIT first?
- Training squemes:
     - Guided: it uses real y_t at training time in the decoder. Poor generalization
     - Unguided: it uses the previos predicted y_t in the decoder
     - Curriculum: combination of guided and unguided
- RETRIEVE THE MODEL
- In trai loss and train rmse file the last one is on the 10%

****  DATA *****
- Dates of the sample (summer, winter?) July 3rd to December 29th
- check if there are more than 3 consecutive 0s not in midnight

- Buildings with MOST VALUES = 0 : OO, 
- 4296 points in time = ~178 days = 1/2 year
- Instancias? = ~4200 If we filter bad instances -> 143
- Hourly/Daily
- We are trimming the data from November 20th 2018 to November 26th 2018 as it was the holiday week.
- for missing values and zeros
	we have replace these value using surrounding data with the help of linear regression
	if the datasets are 2,0,0,5, we replaced it with 2,3,4,5 (as 3 and 4 comes in between using linear regression) 
- Removing outliers (a better model can be done such as getting rid of the values bigger than mean+2variance)
     -BN: 1355: 260090 -> 1050
          1524
     -BR: 320:  327730  -> 300
          3035: 127790 -> 350
     -GE 2194: 281020 -> 155
     - Filtering all >2000 hourly and >100000 for daily
     - When the loss test is smaller than the training loss then review the data to decide wether to get rid of instances of all 0s or replace 0 by  other values
     - which are the buildings that have mostly 0s and we are not take into account


******** SOME ARGUMENTS *********
- Whene training for more iterations (1000 vs 10000) the loss function improves a lot but not necessarily the RMSE
- Markov models provide valueable insight but depend on parameters such as sampling rate, mobility and location


******** FOLDER STRUCTURES *******
- Data : This folder contains all the generated building wise data on both hourly and daily basis
- preprocessing : This folder contains code to preprocessing the data before runing the model.
- model : This folder contains the code for models like linear regression, gcrf, arima
- Results : This folder contains all the generated results model and building wise  


******** HOW TO RUN ********
- Add the preprocessing files path (respectively to your folder) to the PYTHONPATH variable
     export PYTHONPATH=$PYTHONPATH:/home/gissella/Documents/Research/WaterQuality/Binghamton
- The library pmdarima was replaced by pyramid
     from pmdarima.arima import auto_arima
     from pyramid.arima import auto_arima
- for running the linear , arima and gcrf
    - Run the file split.py from folder preprocessing
     - check the data path of generated files and update the current_data_path in global_var.py
     - go to model and run each individual corresponding model file (arima_response, gcrf_response, linear_response)
     - get the results for each building in the Results folder
