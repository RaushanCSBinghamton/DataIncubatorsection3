#!/bin/bash
#SBATCH -J gcrfCPU
### no need SBATCH -w, --nodelist=compute124
echo "starting own vrnn"
source activate tf_down_py2
export PYTHONPATH=$PYTHONPATH:/data/home/gbejara1/Documents/Research/waterproject19_3
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/BN.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/BR.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/C4.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/DE.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/DG.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
python model/gcrf_response.py --fileName Data/processed_data/Hourly/EB.csv --input-dim 3 --inputCols CDH --path Results/Hourly/gcrf
python model/gcrf_response.py --fileName Data/processed_data/Hourly/FA.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/GE.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/JS.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
python model/gcrf_response.py --fileName Data/processed_data/Hourly/LH.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/RA.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
python model/gcrf_response.py --fileName Data/processed_data/Hourly/S2.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/S3.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
#python model/gcrf_response.py --fileName Data/processed_data/Hourly/SN.csv --input-dim 3 --inputCols CHW --path Results/Hourly/gcrf
echo "ending"
