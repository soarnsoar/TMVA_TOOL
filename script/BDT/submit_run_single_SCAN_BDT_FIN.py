#!/usr/bin/env python3
import time
import os
import sys
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)



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


def SubmitFin(version,channel,year,transform,BoostType,BoostTypeOpt,BoostTypeOptValue,NTrees,MaxDepth,MinNodeSize,UseBaggedBoost,UseBaggedBoostOpt,UseBaggedBoostOptValue,SeparationType,nCuts,IgnoreNegWeightsInTraining,analyzer):


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
    WORKDIR="WORKDIR_FIN/"+ "/".join([version,year,channel,transform,BoostType,BoostTypeOpt+"__"+BoostTypeOptValue,"NTrees__"+NTrees,"MaxDepth__"+MaxDepth,"MinNodeSize__"+MinNodeSize,"UseBaggedBoost__"+UseBaggedBoost,UseBaggedBoostOpt+"__"+UseBaggedBoostOptValue,"SeparationType__"+SeparationType,"nCuts__"+nCuts,"IgnoreNegWeightsInTraining__"+IgnoreNegWeightsInTraining])

    
    command=MakeCommand(WORKDIR,this_opt,False)
    submit=1
    Export(WORKDIR,command,"FIN_BDT_"+channel+"_"+str(version)+"_"+year,submit,1)

analyzer="EEMu_MuMuE_Method"
version="2608.2"

dict_submit={
    'muon':{
        '2016preVFP':{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.005', 'NTrees': '500', 'MaxDepth': '5', 'MinNodeSize': '1', 'UseBaggedBoost': 'True', 'BaggedSampleFraction': '0.2', 'SeparationType': 'CrossEntropy', 'nCuts': '30', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.7524418403481035, 'sigeff_B0p3': [0.676, 0.693], 'sigeff_B0p1': [0.382,0.389], 'sigeff_B0p01': [0.082, 0.101]},
        '2016postVFP':{'Trf': 'I', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.005', 'NTrees': '500', 'MaxDepth': '4', 'MinNodeSize': '0.1', 'UseBaggedBoost': 'True', 'BaggedSampleFraction': '0.2', 'SeparationType': 'CrossEntropy', 'nCuts': '50', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.7538683352211905, 'sigeff_B0p3': [0.676, 0.71], 'sigeff_B0p1': [0.393, 0.422], 'sigeff_B0p01': [0.098, 0.12]},
        "2017":{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.001', 'NTrees': '3000', 'MaxDepth': '6', 'MinNodeSize': '0.5', 'UseBaggedBoost': 'True', 'BaggedSampleFraction':'0.4', 'SeparationType': 'CrossEntropy', 'nCuts': '40', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.7538842748190708, 'sigeff_B0p3': [0.677, 0.699], 'sigeff_B0p1': [0.38, 0.417], 'sigeff_B0p01': [0.088, 0.106]},
        "2018":{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.005', 'NTrees': '1000', 'MaxDepth': '6', 'MinNodeSize': '1', 'UseBaggedBoost': 'True', 'BaggedSampleFraction': '0.6', 'SeparationType': 'CrossEntropy', 'nCuts': '20', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.7550193306431433, 'sigeff_B0p3': [0.679, 0.692], 'sigeff_B0p1': [0.385, 0.425], 'sigeff_B0p01': [0.089, 0.103]}
    },
    'electron':{
        '2016preVFP':{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.005', 'NTrees': '800', 'MaxDepth': '4', 'MinNodeSize': '1', 'UseBaggedBoost': 'True', 'BaggedSampleFraction': '0.1', 'SeparationType': 'CrossEntropy', 'nCuts': '10', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.699832425178084, 'sigeff_B0p3': [0.592, 0.59], 'sigeff_B0p1': [0.301, 0.293], 'sigeff_B0p01': [0.051, 0.063]},
        '2016postVFP':{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.01', 'NTrees': '500', 'MaxDepth': '4', 'MinNodeSize': '2.5', 'UseBaggedBoost': 'True', 'BaggedSampleFraction': '0.5', 'SeparationType': 'GiniIndex', 'nCuts': '30', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.7042025463210984, 'sigeff_B0p3': [0.597, 0.61], 'sigeff_B0p1': [0.3, 0.332], 'sigeff_B0p01': [0.062, 0.061]},
        '2017':{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.01', 'NTrees': '1000', 'MaxDepth': '4', 'MinNodeSize': '2.5', 'UseBaggedBoost': 'True', 'BaggedSampleFraction': '0.6', 'SeparationType': 'CrossEntropy', 'nCuts': '20', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.7193983866183472, 'sigeff_B0p3': [0.622, 0.646], 'sigeff_B0p1': [0.322, 0.348], 'sigeff_B0p01': [0.064, 0.073]},
        '2018':{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.01', 'NTrees': '1000', 'MaxDepth': '4', 'MinNodeSize': '2.5', 'UseBaggedBoost': 'True', 'BaggedSampleFraction': '0.6', 'SeparationType': 'CrossEntropy', 'nCuts': '30', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.7143850462252161, 'sigeff_B0p3': [0.613, 0.632], 'sigeff_B0p1': [0.318, 0.343], 'sigeff_B0p01': [0.064, 0.078]},            
    },
    'jet':{
        '2016preVFP':{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.01', 'NTrees': '1500', 'MaxDepth': '4', 'MinNodeSize': '0.1', 'UseBaggedBoost': 'True', 'BaggedSampleFraction': '0.6', 'SeparationType': 'CrossEntropy', 'nCuts': '80', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.5982152587696661, 'sigeff_B0p3': [0.444, 0.451], 'sigeff_B0p1': [0.189, 0.199], 'sigeff_B0p01': [0.027, 0.033]},
        '2016postVFP':{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.01', 'NTrees': '800', 'MaxDepth': '4', 'MinNodeSize': '0.1', 'UseBaggedBoost': 'True', 'BaggedSampleFraction': '0.5', 'SeparationType': 'CrossEntropy', 'nCuts': '50', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.598380415466963, 'sigeff_B0p3': [0.444, 0.449], 'sigeff_B0p1': [0.188, 0.2], 'sigeff_B0p01': [0.026, 0.03]},
        '2017':{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.1', 'NTrees': '50', 'MaxDepth': '6', 'MinNodeSize': '0.1', 'UseBaggedBoost': 'False', 'BaggedSampleFraction': '1', 'SeparationType': 'CrossEntropy', 'nCuts': '40', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.6011577063767876, 'sigeff_B0p3': [0.449, 0.458], 'sigeff_B0p1': [0.193, 0.202], 'sigeff_B0p01': [0.022, 0.024]},
        '2018':{'Trf': 'G', 'BoostType': 'Grad', 'Shrinkage__AdaBoostBeta': '0.1', 'NTrees': '50', 'MaxDepth': '6', 'MinNodeSize': '0.1', 'UseBaggedBoost': 'False', 'BaggedSampleFraction': '1', 'SeparationType': 'CrossEntropy', 'nCuts': '30', 'IgnoreNegWeightsInTraining': 'True', 'auc': 0.600633214899196, 'sigeff_B0p3': [0.448, 0.455], 'sigeff_B0p1': [0.193, 0.201], 'sigeff_B0p01': [0.022, 0.024]}
        
    }
}

#def SubmitFin(version,channel,year,transform,BoostType,BoostTypeOpt,BoostTypeOptValue,NTrees,MaxDepth,MinNodeSize,UseBaggedBoost,UseBaggedBoostOpt,UseBaggedBoostOptValue,SeparationType,nCuts,IgnoreNegWeightsInTraining,analyzer):

BoostTypeOpt='Shrinkage'
UseBaggedBoostOpt='BaggedSampleFraction'
for channel in dict_submit:
    for year in dict_submit[channel]:
        this_dict=dict_submit[channel][year]
        transform=this_dict['Trf']
        BoostType=this_dict['BoostType']

        BoostTypeOptValue=this_dict['Shrinkage__AdaBoostBeta']
        NTrees=this_dict['NTrees']
        MaxDepth=this_dict['MaxDepth']
        MinNodeSize=this_dict['MinNodeSize']
        UseBaggedBoost=this_dict['UseBaggedBoost']
        UseBaggedBoostOptValue=this_dict['BaggedSampleFraction']
        SeparationType=this_dict['SeparationType']
        nCuts=this_dict['nCuts']
        IgnoreNegWeightsInTraining=this_dict['IgnoreNegWeightsInTraining']
        ###
        
        SubmitFin(version,channel,year,transform,BoostType,BoostTypeOpt,BoostTypeOptValue,NTrees,MaxDepth,MinNodeSize,UseBaggedBoost,UseBaggedBoostOpt,UseBaggedBoostOptValue,SeparationType,nCuts,IgnoreNegWeightsInTraining,analyzer)
