#!/usr/bin/env python3

import os
from ExportShellCondorSetup_tamsa import Export
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()

curdir=os.getcwd()

def MakeCommand(workdir,option,ToRemove):
    commandlist=[
        "cd "+curdir,
        "cd "+workdir,
        "python3 "+maindir+"/script/BDT/run_single_BDT.py "+option,
    ]
    if ToRemove:
        commandlist.append("rm -rf "+ToRemove)
     
    ret="&&".join(commandlist)
    return ret



##---1st
list_BoostType=["AdaBoost","Grad"]
list_AdaBoostBeta=['0.5', '0.3', '0.7',] ## Only For AdaBoost
#list_Shrinkage=['1' ,'0.1', '0.05', '0.01'] ## Only For Grad
list_Shrinkage=['1' ,'0.1',]

list_NTrees=['500', '800', '1000']
list_MaxDepth=['2','3','4']

list_MinNodeSize=['2.5', '5', '10']


list_UseBaggedBoost=['True','False']
list_BaggedSampleFraction=['0.4', '0.5', '0.6']
list_SeparationType=["GiniIndex","SDivSqrtSPlusB","CrossEntropy"]

list_nCuts=['10','20','30']
#list_IgnoreNegWeightsInTraining=['True','False']
list_IgnoreNegWeightsInTraining=['True']


transforms=["I","G","U","P","N"]
channels=["muon","electron","jet"]
years=["2016preVFP","2016postVFP","2017","2018"]
analyzer="EEMu_MuMuE_Method"
version="2409.2"



submit=False

dict_BoostType={
    "AdaBoost":{"AdaBoostBeta":list_AdaBoostBeta},
    "Grad":{"Shrinkage":list_Shrinkage},    
}
dict_UseBaggedBoost={
    "True":{"BaggedSampleFraction":list_BaggedSampleFraction},
    "False":{"BaggedSampleFraction":["0"]}
    }


ntotal=len(channels)*len(years)*(len(list_AdaBoostBeta)+len(list_Shrinkage))*(1+len(list_BaggedSampleFraction))*len(list_NTrees)*len(list_MaxDepth)*len(list_MinNodeSize)*len(list_SeparationType)*len(list_nCuts)*len(list_IgnoreNegWeightsInTraining)
print("ntotal=",ntotal)
for channel in channels:
    #break
    for year in years:
        for transform in transforms:
            for BoostType in dict_BoostType:
                for BoostTypeOpt in dict_BoostType[BoostType]:
                    #BoostTypeOpt = "AdaBoostBeta"
                    for BoostTypeOptValue in dict_BoostType[BoostType][BoostTypeOpt]:
                        for NTrees in list_NTrees:
                            for MaxDepth in list_MaxDepth:
                                for MinNodeSize in list_MinNodeSize:
                                    for UseBaggedBoost in dict_UseBaggedBoost:
                                        for UseBaggedBoostOpt in dict_UseBaggedBoost[UseBaggedBoost]:
                                            for UseBaggedBoostOptValue in dict_UseBaggedBoost[UseBaggedBoost][UseBaggedBoostOpt]:
                                                for SeparationType in list_SeparationType:
                                                    for nCuts in list_nCuts:
                                                        for IgnoreNegWeightsInTraining in list_IgnoreNegWeightsInTraining:
                                                            name="__".join([channel,year,transform,BoostType])
                                                            this_opt=" --transform "+transform\
                                                                +" --BoostType "+BoostType\
                                                                +" --"+BoostTypeOpt+" "+BoostTypeOptValue\
                                                                +" --NTrees "+NTrees\
                                                                +" --MaxDepth "+MaxDepth\
                                                                +" --MinNodeSize "+MinNodeSize\
                                                                +" --UseBaggedBoost "+UseBaggedBoost\
                                                                +" --"+UseBaggedBoostOpt+" "+UseBaggedBoostOptValue\
                                                                +" --SeparationType "+SeparationType\
                                                                +" --nCuts "+nCuts\
                                                                +" --IgnoreNegWeightsInTraining "+IgnoreNegWeightsInTraining\
                                                                +" --analyzer "+analyzer\
                                                                +" --version "+version\
                                                                +" --name BDT_"+year
                                                            
                                                            print(this_opt)
                                                            WORKDIR="WORKDIR/"+ "/".join([version,year,channel,transform,BoostType,BoostTypeOpt+"__"+BoostTypeOptValue,NTrees+"__"+NTrees,"MaxDepth__"+MaxDepth,"MinNodeSize__"+MinNodeSize,"UseBaggedBoost__"+UseBaggedBoost,UseBaggedBoostOpt+"__"+UseBaggedBoostOptValue,"SeparationType__"+SeparationType,"nCuts__"+nCuts,"IgnoreNegWeightsInTraining__"+IgnoreNegWeightsInTraining])
                                                            
                                                            command=MakeCommand(WORKDIR,this_opt,"BDT_"+year+"*")
                                                            Export(WORKDIR,command,"BDT_"+channel+"_"+str(version)+"_"+year,submit,1)

                                                            exit(1)
