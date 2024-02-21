import uproot as up
import argparse
import glob
import awkward as ak
from numba import jit
import numpy as np
from tqdm import tqdm
from vector import Vector  # Correct import
import matplotlib
import matplotlib.pyplot as plt
import mplhep as hep
hep.style.use("CMS")

import time
start_time = time.time()

def read_data(file_list):
	
	# using input args
	flist=[]
	for f in file_list:
		flist.append(f + ':ntuple/tree')
	branches = ["Ele_Esct",                       
                    "Ele_etaSC",                     
                    "Ele_phiSC",                     
                    "Ele_ecalDriven",                
                    "Ele_charge",                    
                    "Ele_dEtaSeed",                  
                    "Ele_dPhiIn",                    
                    "Ele_full5x5_sigmaIetaIeta",    
                    "Ele_passVetoId",   
                    "Ele_passLooseId",  
                    "Ele_passMediumId", 
                    "Ele_passTightId",  
                    "Ele_passHEEPId",   
                    "Ele_isMatchTrue",  
                    "Ele_genPartFlav",  
                    "genMET",           
                    "isHLTEle30Pass",   
                    "isHLTEle35Pass",   
                    "isHLTEle115Pass",  
                    "isHLTPho200Pass",  
                    "istrgMatchTrue"]

	return flist, branches

def Loop(flist,brancher):

	# define array
	histo={}
	print(flist)

	# --Start File Loop
	for arrays in up.iterate(flist,branches): #  for Uproot4
                # Zipping the arrays
                Ele = ak.zip(
                {
                    "Et"                        : arrays["Ele_Esct"],                       
                    "etaSC"                     : arrays["Ele_etaSC"],                     
                    "phiSC"                     : arrays["Ele_phiSC"],                     
                    "ecalDriven"                : arrays["Ele_ecalDriven"],                
                    "charge"                    : arrays["Ele_charge"],                    
                    "dEtaSeed"                  : arrays["Ele_dEtaSeed"],                  
                    "dPhiIn"                    : arrays["Ele_dPhiIn"],                    
                    "full5x5_sigmaIetaIeta"     : arrays["Ele_full5x5_sigmaIetaIeta"],    
                    #"passVetoId"                : arrays["Ele_passVetoId"],   
                    #"passLooseId"               : arrays["Ele_passLooseId"],  
                    #"passMediumId"              : arrays["Ele_passMediumId"], 
                    "passTightId"               : arrays["Ele_passTightId"],  
                    "passHEEPId"                : arrays["Ele_passHEEPId"],   
                    "isMatchTrue"               : arrays["Ele_isMatchTrue"],  
                    "genPartFlav"               : arrays["Ele_genPartFlav"],  
                })
                
                MET = ak.zip({
                     "genMET"                    : arrays["genMET"],           
               #      "genPhi"                    : arrays["genMET_Phi"],       
               #      "pfMET"                     : arrays["pfMET"],            
               #      "pfPhi"                     : arrays["pfMET_Phi"],        
               #      "puppiMET"                  : arrays["puppiMET"],         
                })
                
                HLT = ak.zip(
                {
                    "Ele30Pass"                 : arrays["isHLTEle30Pass"],   
                    "Ele35Pass"                 : arrays["isHLTEle35Pass"],   
                    "Ele115Pass"                : arrays["isHLTEle115Pass"],  
                    "Pho200Pass"                : arrays["isHLTPho200Pass"],  
                    "isMatch"                   : arrays["istrgMatchTrue"],
                })

                def cut(candidates): #already cut applied at masking # 5
                    return candidates[
                        (candidates.Et > 35. & abs(candidates.etaSC) < 1.444 )
                    ]

                ### 1 Apply Trigger
                from itertools import combinations, product

                print("--------Masking check --------------------")  
                print("### Number of event       : ",len(MET.genMET))
                print("### Total Num of electron : ",len(Ele.Et), " , Et= ", Ele.Et)

                hlt_mask = (HLT.isMatch == 1)
                electrons = Ele[hlt_mask]
                print("### 1 hlt mask            : ", len(electrons.Et), " , Et= ", electrons.Et)

                zcands = ak.combinations(Ele, 2, fields=["tag", "probe"])
                print("### 2  diele mask         : ", len(zcands.tag.Et), " , Et= ", zcands.tag.Et)

                zcands = zcands[
                    (zcands.tag.Et >= 35.)
                    & (abs(zcands.tag.etaSC) < 1.444) #np.abs(Electron.eta + Electron.deltaEtaSC) < 1.479
                    & (zcands.tag.passTightId == 1)
                ]

                # filter out events that have no z candidates
                zcands = zcands[ak.num(zcands) > 0]
                print("### 3 tag tight id mask   : ", len(zcands.tag.Et), " , ", zcands.tag.Et)

                # some events may have multiple candidates, take the leading one (as they are sorted by Et)
                zcands = ak.firsts(zcands)
                print("### 4 ak.first tnp mask   : ", len(zcands.tag.Et), " , ", zcands.tag.Et)

                # compute invariant mass
                #mass = (zcands.tag + zcands.probe).mass
                goodprobe = (zcands.tag.charge * zcands.probe.charge < 0) & (zcands.probe.Et >= 35.) & (abs(zcands.probe.etaSC) < 1.444)

                print("### 5 probe q et EB mask  : ", len(zcands.probe[goodprobe].Et), " , Et= ",zcands.probe[goodprobe].Et )
                electrons = zcands.probe[goodprobe]

                #fig, (axp, axf) = plt.subplots(1, 2, sharey=True, figsize=(12, 6))
                #mbins = np.linspace(60, 200, 141)
                #axp.hist(mass[goodprobe], bins=mbins)
                #axp.set_title('HEEP Passing probes')
                #axp.set_ylabel('Events')
                #axp.set_xlabel('Dielectron mass (GeV)')
                ##axf.hist(mass[~goodprobe], bins=mbins)
                ##axf.set_title('HEEP Failing probes')
                ##axf.set_xlabel('Dielectron mass (GeV)')
                ##plt.show()
                ##return zcands, goodprobe

                flavors, counts = np.unique(ak.to_numpy(electrons.genPartFlav), return_counts=True)
                for flavor, count in zip(flavors, counts):
                    print("### 7 GenPart flavor % 3d has % 8d occurrences" % (flavor, count))
                
                prompt_el    = electrons[electrons.genPartFlav == 1 ] 
                nonprompt    = electrons[electrons.genPartFlav != 1 ]  
                tau_eles     = electrons[electrons.genPartFlav == 15] 
                photon_fakes = electrons[electrons.genPartFlav == 22] 
                b_eles       = electrons[electrons.genPartFlav == 5 ] 
                c_eles       = electrons[electrons.genPartFlav == 4 ]
                lightq_eles  = electrons[electrons.genPartFlav == 3 ]
                unmatched    = electrons[electrons.genPartFlav == 0 ]

                ## Prepare histogram
                h_Et_s          = ak.to_numpy(prompt_el.Et                        )
                h_Et_b          = ak.to_numpy(nonprompt.Et                        )
                h_etaSC_s       = ak.to_numpy(prompt_el.etaSC                     )
                h_etaSC_b       = ak.to_numpy(nonprompt.etaSC                     )
                h_passTightId_s = ak.to_numpy(prompt_el.passTightId               ) 
                h_passTightId_b = ak.to_numpy(nonprompt.passTightId               ) 
                h_passHEEPId_s  = ak.to_numpy(prompt_el.passHEEPId                )  
                h_passHEEPId_b  = ak.to_numpy(nonprompt.passHEEPId                )  

                if len(histo) == 0:
                        histo['Et_s']               = h_Et_s              
                        histo['Et_b']               = h_Et_b           
                        histo['etaSC_s']            = h_etaSC_s           
                        histo['etaSC_b']            = h_etaSC_b        
                        histo['passTightId_s']      = h_passTightId_s     
                        histo['passTightId_b']      = h_passTightId_b  
                        histo['passHEEPId_s']       = h_passHEEPId_s      
                        histo['passHEEPId_b']       = h_passHEEPId_b   
                else:
                        histo['Et_s']               = np.concatenate((histo['Et_s']              , h_Et_s              ),axis=0)    
                        histo['Et_b']               = np.concatenate((histo['Et_b']              , h_Et_b              ),axis=0) 
                        histo['etaSC_s']            = np.concatenate((histo['etaSC_s']           , h_etaSC_s           ),axis=0)   
                        histo['etaSC_b']            = np.concatenate((histo['etaSC_b']           , h_etaSC_b           ),axis=0)   
                        histo['passTightId_s']      = np.concatenate((histo['passTightId_s']     , h_passTightId_s     ),axis=0)     
                        histo['passTightId_b']      = np.concatenate((histo['passTightId_b']     , h_passTightId_b     ),axis=0)  
                        histo['passHEEPId_s']       = np.concatenate((histo['passHEEPId_s']      , h_passHEEPId_s      ),axis=0)   
                        histo['passHEEPId_b']       = np.concatenate((histo['passHEEPId_b']      , h_passHEEPId_b      ),axis=0) 

                return histo

if __name__ == "__main__":

         parser = argparse.ArgumentParser()
         parser.add_argument(nargs='+' ,help='input files', dest='filename')
         parser.add_argument('--outname', '-o', help='outname')
         args  =parser.parse_args()
         start_time = time.time()
         flist, branches = read_data(args.filename)

         histo = Loop(flist,branches)
         
         outname = args.outname
         print("outname = ", outname)
         np.save(outname,histo,allow_pickle=True)
         print("--- %s seconds ---" % (time.time() - start_time))
