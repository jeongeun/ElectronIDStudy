import uproot as up
import argparse
import glob
import awkward as ak
from numba import jit
import numpy as np
from tqdm import tqdm
from statsmodels.stats.proportion import proportion_confint
#from vector import Vector  # Correct import
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import mplhep as hep
hep.style.use("CMS")

def collect(arr_sig, arr_bkg, file_name):  # Array, Name, x_min, x_max, bin-number
    data_sig = []
    data_bkg = []
    data_sig = arr_sig
    data_bkg = arr_bkg
    return data_sig, data_bkg

def drawEff(tot_s, tot_b, cut_s, cut_b, title, xmin, xmax, bin, save):
    
    bins = np.linspace(xmin, xmax, bin)

    hist_tot_s, _ = np.histogram(tot_s, bins=bins)
    hist_cut_s, _ = np.histogram(cut_s, bins=bins)
    hist_tot_b, _ = np.histogram(tot_b, bins=bins)
    hist_cut_b, _ = np.histogram(cut_b, bins=bins)
    
    cl95 = 0.95
    lower_s, upper_s = proportion_confint(hist_cut_s, hist_tot_s, alpha=1-cl95, method='beta')
    lower_b, upper_b = proportion_confint(hist_cut_b, hist_tot_b, alpha=1-cl95, method='beta')
    efficiency_s = hist_cut_s / hist_tot_s
    error_s = (upper_s - lower_s) / 2
    efficiency_b = hist_cut_b / hist_tot_b
    error_b = (upper_b - lower_b) / 2
    ## error_s = np.sqrt(efficiency_s * (1 - efficiency_s) / hist_tot_s) # binomial err
    ## error_b = np.sqrt(efficiency_b * (1 - efficiency_b) / hist_tot_b) # binomial err

    bin_centers = (bins[:-1] + bins[1:]) / 2
    
    # ROOT-like format
    plt.style.use(hep.style.ROOT)
    plt.figure(figsize=(8, 8))  # Figure size
    
    common_opts = {
       #'alpha': 0.5,
       'fmt' : 'o',
       'linestyle': '',
       #'linewidth':2.0,
    }
    # Draw histogram
    hep.cms.label(fontsize=20, data=False, loc=0, year='Run3', com=13.6)
    plt.errorbar(bin_centers, efficiency_s, yerr=error_s, color='blue', label='Prompt electron', **common_opts)
    plt.errorbar(bin_centers, efficiency_b, yerr=error_b, color='red' , label='Nonprompt'      , **common_opts)
    plt.ylim(0.0, 1.01)
    plt.xticks(fontsize=16)  # xtick size
    plt.xlabel(r'Electron ' + title, fontsize=25)  # X-label
    plt.ylabel("Efficiency", fontsize=25)  # Y-label
    plt.yticks(fontsize=16)  # ytick size
    plt.grid(alpha=0.5)  # grid
    plt.legend(loc='best', prop={"size": 20})  # show legend
    outname_fig = save + ".png" 
    plt.savefig(outname_fig)
    #plt.show()  # show histogram
    plt.close()

if __name__ == "__main__":

         file_names_nocut = ['comb_npy_noanycut/Comb_DY50_new.npy', 'comb_npy_noanycut/Comb_DY120_new.npy', 'comb_npy_noanycut/Comb_DY200_new.npy', 'comb_npy_noanycut/Comb_DY400_new.npy', 'comb_npy_noanycut/Comb_DY800_new.npy', 'comb_npy_noanycut/Comb_DY1500_new.npy','comb_npy_noanycut/Comb_DY2500_new.npy', 'comb_npy_noanycut/Comb_DY4000_new.npy', 'comb_npy_noanycut/Comb_DY6000_new.npy', 'comb_npy_noanycut/Comb_GJet_new.npy','comb_npy_noanycut/Comb_QCD1000_new.npy','comb_npy_noanycut/Comb_QCD120_new.npy','comb_npy_noanycut/Comb_QCD1400_new.npy','comb_npy_noanycut/Comb_QCD170_new.npy','comb_npy_noanycut/Comb_QCD1800_new.npy','comb_npy_noanycut/Comb_QCD2400_new.npy','comb_npy_noanycut/Comb_QCD300_new.npy','comb_npy_noanycut/Comb_QCD3200_new.npy']

         file_names_noisocut = ['comb_npy_fullheep/Comb_DY50_new.npy', 'comb_npy_fullheep/Comb_DY120_new.npy', 'comb_npy_fullheep/Comb_DY200_new.npy', 'comb_npy_fullheep/Comb_DY400_new.npy', 'comb_npy_fullheep/Comb_DY800_new.npy', 'comb_npy_fullheep/Comb_DY1500_new.npy','comb_npy_fullheep/Comb_DY2500_new.npy', 'comb_npy_fullheep/Comb_DY4000_new.npy', 'comb_npy_fullheep/Comb_DY6000_new.npy', 'comb_npy_fullheep/Comb_GJet_new.npy','comb_npy_fullheep/Comb_QCD1000_new.npy','comb_npy_fullheep/Comb_QCD120_new.npy','comb_npy_fullheep/Comb_QCD1400_new.npy','comb_npy_fullheep/Comb_QCD170_new.npy','comb_npy_fullheep/Comb_QCD1800_new.npy','comb_npy_fullheep/Comb_QCD2400_new.npy','comb_npy_fullheep/Comb_QCD300_new.npy','comb_npy_fullheep/Comb_QCD3200_new.npy']
         lumi = 1
         #eventWeights = {
         #     'Comb_DY50_new.npy'   : 2.219e+03 / 10403118.0 * lumi, 
         #     'Comb_DY120_new.npy'  : 2.165e+01 / 5238528.0  * lumi,
         #     'Comb_DY200_new.npy'  : 3.058e+00 / 3147891.0  * lumi,   
         #     'Comb_DY400_new.npy'  : 2.691e-01 / 2989350.0  * lumi,  
         #     'Comb_DY800_new.npy'  : 1.915e-02 / 2004300.0  * lumi,  
         #     'Comb_DY1500_new.npy' : 1.111e-03 / 2053944.0  * lumi,   
         #     'Comb_DY2500_new.npy' : 5.949e-05 / 986496.0   * lumi, 
         #     'Comb_DY4000_new.npy' : 1.558e-06 / 1027656.0  * lumi,  
         #     'Comb_DY6000_new.npy' : 3.519e-08 / 550816.0   * lumi, 
         #     'Comb_GJet_new.npy'    : 2.957e+05 / 30081000.0 * lumi,
         #     'Comb_QCD120_new.npy'  : 7.142e+04 / 3255573.0  * lumi,
         #     'Comb_QCD170_new.npy'  : 1.796e+04 / 3542697.0  * lumi,
         #     'Comb_QCD300_new.npy'  : 1.221e+03 / 3254133.0  * lumi,
         #     'Comb_QCD1000_new.npy' : 8.944e+00 / 8134126.0  * lumi,
         #     'Comb_QCD1400_new.npy' : 8.097e-01 / 4289440.0  * lumi,
         #     'Comb_QCD1800_new.npy' : 1.152e-01 / 2453207.0  * lumi,
         #     'Comb_QCD2400_new.npy' : 7.592e-03 / 789885.0  * lumi,
         #     'Comb_QCD3200_new.npy' : 2.311e-04 / 473821.0   * lumi,
         #}

# Accumulators for data and weights
         # Load data and prepare weights
         allEt_sig = []
         allEt_bkg = []
         allsieie_sig = []
         allsieie_bkg = []
         alletaSC_sig = []
         alletaSC_bkg = []
         allpassTightId_sig = []            
         allpassTightId_bkg = []            
         allpassHEEPId_sig = []            
         allpassHEEPId_bkg = []            

         for file_name in file_names_nocut:
             loaded_dict = np.load(file_name, allow_pickle=True).item()  # Using .item() to get the dictionary

             Et_sig, Et_bkg = collect(loaded_dict['Et_s'], loaded_dict['Et_b'], file_name)
             allEt_sig  = np.concatenate((allEt_sig  ,Et_sig ))
             allEt_bkg  = np.concatenate((allEt_bkg  ,Et_bkg ))
             #print("filename ", file_name , "  allEt_sig " , allEt_sig , "  len(arr) ", len(allEt_sig)) 
             sieie_sig, sieie_bkg = collect(loaded_dict['sieie_s'], loaded_dict['sieie_b'], file_name)
             allsieie_sig  = np.concatenate((allsieie_sig  ,sieie_sig ))
             allsieie_bkg  = np.concatenate((allsieie_bkg  ,sieie_bkg ))
             
             etaSC_sig, etaSC_bkg = collect(loaded_dict['etaSC_s'], loaded_dict['etaSC_b'], file_name)
             alletaSC_sig  = np.concatenate((alletaSC_sig  ,etaSC_sig ))
             alletaSC_bkg  = np.concatenate((alletaSC_bkg  ,etaSC_bkg ))
             passTightId_sig, passTightId_bkg = collect(loaded_dict['passTightId_s'], loaded_dict['passTightId_b'], file_name)
             allpassTightId_sig  = np.concatenate((allpassTightId_sig  ,passTightId_sig ))
             allpassTightId_bkg  = np.concatenate((allpassTightId_bkg  ,passTightId_bkg ))
             
             passHEEPId_sig, passHEEPId_bkg = collect(loaded_dict['passHEEPId_s'], loaded_dict['passHEEPId_b'], file_name)
             allpassHEEPId_sig  = np.concatenate((allpassHEEPId_sig  ,passHEEPId_sig ))
             allpassHEEPId_bkg  = np.concatenate((allpassHEEPId_bkg  ,passHEEPId_bkg ))

         allEt2_sig = []
         allEt2_bkg = []
         allsieie2_sig = []
         allsieie2_bkg = []
         alletaSC2_sig = []
         alletaSC2_bkg = []
         allpassTightId2_sig = []            
         allpassTightId2_bkg = []            
         allpassHEEPId2_sig = []            
         allpassHEEPId2_bkg = []            
               
         for file_name2 in file_names_noisocut:
             loaded_dict_ = np.load(file_name2, allow_pickle=True).item()  # Using .item() to get the dictionary

             Et2_sig, Et2_bkg = collect(loaded_dict_['Et_s'], loaded_dict_['Et_b'], file_name2)
             allEt2_sig  = np.concatenate((allEt2_sig  ,Et2_sig ))
             allEt2_bkg  = np.concatenate((allEt2_bkg  ,Et2_bkg ))
             #print("filename ", file_name2 , "  allEt2_sig " , allEt2_sig , "  len(arr) ", len(allEt2_sig)) 
             sieie2_sig, sieie2_bkg = collect(loaded_dict_['sieie_s'], loaded_dict_['sieie_b'], file_name2)
             allsieie2_sig  = np.concatenate((allsieie2_sig  ,sieie2_sig ))
             allsieie2_bkg  = np.concatenate((allsieie2_bkg  ,sieie2_bkg ))
             
             etaSC2_sig, etaSC2_bkg = collect(loaded_dict_['etaSC_s'], loaded_dict_['etaSC_b'], file_name2)
             alletaSC2_sig  = np.concatenate((alletaSC2_sig  ,etaSC2_sig ))
             alletaSC2_bkg  = np.concatenate((alletaSC2_bkg  ,etaSC2_bkg ))
 
             passTightId2_sig, passTightId2_bkg = collect(loaded_dict_['passTightId_s'], loaded_dict_['passTightId_b'], file_name2)
             allpassTightId2_sig  = np.concatenate((allpassTightId2_sig  ,passTightId2_sig ))
             allpassTightId2_bkg  = np.concatenate((allpassTightId2_bkg  ,passTightId2_bkg ))
             
             passHEEPId2_sig, passHEEPId2_bkg = collect(loaded_dict_['passHEEPId_s'], loaded_dict_['passHEEPId_b'], file_name2)
             allpassHEEPId2_sig  = np.concatenate((allpassHEEPId2_sig  ,passHEEPId2_sig ))
             allpassHEEPId2_bkg  = np.concatenate((allpassHEEPId2_bkg  ,passHEEPId2_bkg ))
               
#### DRAW #######
         drawEff(allEt_sig, allEt_bkg  , allEt2_sig, allEt2_bkg  , "$E_{T}$ (GeV)" , 0.0, 5000, 50, "eff_Et")
         drawEff(alletaSC_sig, alletaSC_bkg , alletaSC2_sig , alletaSC2_bkg, "$\eta_{SC}$"              , -3.0, 3.0, 40, "eff_etaSC")
         drawEff(allsieie_sig, allsieie_bkg , allsieie2_sig , allsieie2_bkg, "$\sigma_{i \eta i \eta}$" , 0.0, 0.08, 80, "eff_sieie")
