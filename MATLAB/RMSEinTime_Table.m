clc;
clear;

%%%%%%%%%% Parameteres we can change %%%%%%%%%%
%Buildings Names
buildingNames = {'BN','BR','C4','DE','DG','EB','FA','GE','JS','LH','RA','S2','S3','SN'}; % 1x14 cells
%
nBuilds = size(buildingNames,2)
%1. Sequence lengths
prevStepsX=[24 24 24 24];
predStepsY=12;
%2. Limit for axis x
uplimit = 200
%3. Models Names for legends. Real only used for predVSreal
modelNames = {'GCRF C','GCRF CH','GCRF CD','GCRF CDH','Real'}
%{'GCRF 18-12','GCRF 24-12','GCRF 30-12','Real'}
%{'LSTM C','LSTM CW','LSTM CH','LSTM CD','Real'};
%{'GCRF C','GCRF CW','GCRF CH','GCRF CD','Real'};
%{'GCRF CDH','GCRF CHW','GCRF CDW','Real'}
%4. Colors to use in real vs predicted
colors={'g','m','b','r','y','l'}; % real is the last one
%5. Suffix of the file names
suffix = "_gcrf_c_ch_cd_cdh";
%6. day to draw
day = 1;
%7. metric for table
metric = 'rmse'

nModels = size(modelNames,2)
%%%%%% Try not to change anything from here %%%%%%%
filePaths = fopen('pathToFile.txt','r')
fileTable = fopen(strcat('../Images/comparisonTable',suffix,'.txt'),'w');
formatString = {'%s ';'%.2f ';'\n'};
%[C{[1 2*ones(1,8) 3]}]

formatSpec = [formatString{[1*ones(1,nModels-1) 3]}] %'%s %s %s\n';%3*'%s'+'\n';
pathsMatrix = textscan(filePaths,formatSpec,'Delimiter','\t', 'headerLines', 1); %fgets

for i= 1:nBuilds %building = buildingNames %
    modelPlots = cell(1,nModels)
    rmse_maeTime = cell(1,nModels-1) % real not taken into account
    tableComp = [];
    for j=1:nModels-1
        nameFile = strcat(pathsMatrix{j}{i},buildingNames{i},'_',num2str(prevStepsX(j)),'_',num2str(predStepsY))
        real = load(strcat(nameFile,'_real.txt'));
        % check sanity, load other reals
        pred = load(strcat(nameFile,'_pred.txt'));
        modelPlots{1,j} = pred
        modelPlots{1,j+1} = real ;
        %maeList = combined_RE(real, pred, 1,predStepsY)%MAE calculation - 1st, last and AVG
        rmse_mae = load(strcat(nameFile,'_test_',metric,'.txt')); % rmse or mae
        rmse_maeList = [rmse_mae(1),rmse_mae(predStepsY),mean(rmse_mae)]
        rmse_maeTime{1,j} = rmse_mae
        tableComp = [tableComp rmse_maeList];
    end
    
    % Real VS Predicted plot % do a for if want to plot for every day
    plotRealVSPredicted(modelPlots,colors,suffix, day,buildingNames{i},uplimit, modelNames) %real, pred
    plotRMSEtime( rmse_maeTime, suffix , buildingNames{i} , predStepsY , modelNames )
    fprintf(fileTable,[formatString{[1*ones(1,3*nModels-3) 3]}],tableComp); %%  '%f %f %f %f %f %f %f %f %f\n'
end