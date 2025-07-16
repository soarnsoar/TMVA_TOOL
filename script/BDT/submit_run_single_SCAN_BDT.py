#!/usr/bin/env python3
import time
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
list_Shrinkage=['1' ,'0.1', '0.05', '0.01'] ## Only For Grad
#list_Shrinkage=['1' ,'0.1',"0.01"]

list_NTrees=['500', '800', '1000']
#list_NTrees=['500', '1000']
list_MaxDepth=['2','3','4']
#list_MaxDepth=['3']

list_MinNodeSize=['2.5', '5', '10']
#list_MinNodeSize=['5',]


#list_UseBaggedBoost=['False']
list_UseBaggedBoost=['True','False']
list_BaggedSampleFraction=['0.4', '0.5', '0.6']
#list_SeparationType=["GiniIndex","SDivSqrtSPlusB","CrossEntropy"]
list_SeparationType=["GiniIndex","CrossEntropy"]

list_nCuts=['10','20','30']
#list_IgnoreNegWeightsInTraining=['True','False']
list_IgnoreNegWeightsInTraining=['True']


#transforms=["I","G","U","P","N"]
#transforms=["N","G","U","P","I","D"]
transforms=["I","G","U","N"]
channels=["muon","electron","jet"]
#channels=["electron","jet"]
years=["2016postVFP","2016preVFP","2017","2018"]
analyzer="EEMu_MuMuE_Method"
version="2409.2"



##--2nd

#list_Shrinkage=['0.5',"0.05" ,"0.005"]
#list_NTrees=["300","800","1500"]
#list_MaxDepth=["2","4"]
#transforms=["G"]
#list_UseBaggedBoost=["True"]
#list_SeparationType=["GiniIndex","CrossEntropy"]


##--3rd
#list_BoostType=["AdaBoost","Grad"]
#list_BoostType=["AdaBoost"]
#list_AdaBoostBeta=['0.1', '0.2', "0.3","0.4","0.5","0.6" ,'0.7',"0.8"] ## Only For AdaBoost
#list_MaxDepth=["1","2","3","4","5"]
#list_NTrees=["300","400","500","600","700","800","900","1000","1200"]
#list_MinNodeSize=['2.5', '5', '10']
######


submit=1
##-----subopt
dict_BoostType={
    "AdaBoost":{"AdaBoostBeta":list_AdaBoostBeta},
    "Grad":{"Shrinkage":list_Shrinkage},    
}
dict_UseBaggedBoost={
    "True":{"BaggedSampleFraction":list_BaggedSampleFraction},
    "False":{"BaggedSampleFraction":["0"]}
    }


#ntotal=len(channels)*len(years)*len(transforms)*(len(list_AdaBoostBeta)+len(list_Shrinkage))*(1+len(list_BaggedSampleFraction))*len(list_NTrees)*len(list_MaxDepth)*len(list_MinNodeSize)*len(list_SeparationType)*len(list_nCuts)*len(list_IgnoreNegWeightsInTraining)
#print("ntotal=",ntotal)

i_submit=0

for channel in channels:
    #break
    for year in years:
        for transform in transforms:
            for BoostType in dict_BoostType:
                for BoostTypeOpt in dict_BoostType[BoostType]:
                    for BoostTypeOptValue in dict_BoostType[BoostType][BoostTypeOpt]:
                        #BoostTypeOpt = "AdaBoostBeta"
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
                                                                +" --name BDT_"+year\
                                                                +" --year "+year\
                                                                +" --channel "+channel
                                                            
                                                            #print(this_opt)
                                                            WORKDIR="WORKDIR/"+ "/".join([version,year,channel,transform,BoostType,BoostTypeOpt+"__"+BoostTypeOptValue,"NTrees__"+NTrees,"MaxDepth__"+MaxDepth,"MinNodeSize__"+MinNodeSize,"UseBaggedBoost__"+UseBaggedBoost,UseBaggedBoostOpt+"__"+UseBaggedBoostOptValue,"SeparationType__"+SeparationType,"nCuts__"+nCuts,"IgnoreNegWeightsInTraining__"+IgnoreNegWeightsInTraining])
                                                            if os.path.isfile(WORKDIR+"/run.done") : continue
                                                            command=MakeCommand(WORKDIR,this_opt,"BDT_"+year+"*")
                                                            Export(WORKDIR,command,"BDT_"+channel+"_"+str(version)+"_"+year,submit,1)

                                                            i_submit+=1

                                                            if i_submit % 50 == 49 : time.sleep(5)
                                                            #exit(1)
print("i_submit",i_submit)
