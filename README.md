# condasetup

  
conda env list

conda environments:

newenvironment           /u/user/jelee/.conda/envs/newenvironment

base                  *  /usr


$ conda activate newenvironment

# BatchJob : Read Ntuples => Apply TnP cut => Make .npy output
   
(ex) python step1_batch.py [DATASETNAME] [ROOT_DIRECTORY]

$ python step1_batch.py DY50     'condor_DYto2E_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8_D_Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2_D_MINIAODSIM_240128_023941/condorOut/' >& log_dy50.out &

$ python step1_batch.py DY120    'condor_DYto2E_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8_D_Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2_D_MINIAODSIM_240128_023957/condorOut/'  >& log_dy120.out &

$ python step1_batch.py DY200    'condor_DYto2E_MLL-200to400_TuneCP5_13p6TeV_powheg-pythia8_D_Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2_D_MINIAODSIM_240128_024007/condorOut/'  >& log_dy200.out &


# Merge .npy output files

(ex) python step2_merge.py [DATASETNAME] [NUMBER_OF_NPY_OUTPUT_FILES]

$ python step2_merge.py DY50  22

$ python step2_merge.py DY120 11

$ python step2_merge.py DY200 7


# Draw efficiency plot

$ python draweff.py
