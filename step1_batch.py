import uproot as up
import sys
import glob
import awkward as ak
import numpy as np
import subprocess
from vector import Vector  # Correct import
import matplotlib
import mplhep as hep
hep.style.use("CMS")

import time
start_time = time.time()

Base_dir = '/d0/scratch/jelee/workspace/HEEPstudy/CMSSW_13_0_14/src/SimpleNtuplizer/Run3Ntuplizer/test/'

sample = sys.argv[1]
condorName = sys.argv[2]

# using file list
file_list = glob.glob(Base_dir + condorName + "ntuple*.root")

def calc_Nout(maxfile,nfile):
    nfile = maxfile + nfile - 1
    nout = int(nfile / maxfile)
    return(nout)

maxfile = 10 # Max number of input files for each run ( argumnet )
nfile=len(file_list) #  Number of total input files
print("nfile = {}".format(nfile))
nout  = calc_Nout(maxfile,nfile) # Number of output files
print("nout = {}".format(nout))

for i in range(nout):
    start = i*maxfile
    end = start + maxfile

    infiles = (' '.join(file_list[start:end]))
    fn_out = sample + "_" + str(i) + "_new.npy"

    print("############################## SET: ",fn_out)
    print(infiles)

    #Run specific excutable codes
    args = 'python' + ' '+ 'makeROC.py' + ' ' + '--outname' + ' ' + fn_out + ' '+  infiles
    subprocess.call(args,shell=True)
