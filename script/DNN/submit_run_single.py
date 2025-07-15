#!/usr/bin/env python
from GetCommands import GetOptionCommand,MakeCommand
import os
from ExportShellCondorSetup_tamsa import Export
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()

##---1st
nlayers=[5,10,20]
nnodes=[64,128,256]
batchsizes=[100,500,1000]
dropouts=[0.2,0.4,0.6]
nepoch=300
transforms=["I","G","U","P","N"]
versions=["2409.2"]
years=["2016preVFP","2016postVFP","2017","2018"]
analyzers=["EEMu_MuMuE_Method"]
#channels=["muon","electron","jet"]
channels=["jet"]
switches=[False] 
useLOs=[False]

##---2nd
#nlayers=[1,2,3,4,5,6,7]
#nnodes=[50,64,80]
#batchsizes=[90,100,110,120]
#dropouts=[0.1,0.2,0.3]
#nepoch=300
#transforms=["N","N,U","G","G,U","N,G","N,G,U","N,U,G"]

#channels=["muon","electron","jet"]
#channels=["muon","electron"]
#switches=[False] 
#years=["2016preVFP","2016postVFP","2017","2018"]
#analyzers=["EEMu_MuMuE_Method"]


#useLOs=[True, False]
#useLOs=[False]

##--3rd

#nlayers=[1,2,3,4,5]
#nnodes=[50]
#batchsizes=[100]
#dropouts=[0.1,0.2,0.3]
#nepoch=300
#channels=["muon","electron","jet"]
#switches=[False] 
#years=["2016preVFP","2016postVFP","2017","2018"]
#analyzers=["EEMu_MuMuE_Method"]
#transforms=["N","N,U","G","G,U","N,G","N,G,U","N,U,G"]

#useLOs=[True, False]
#useLOs=[False]


submit=True
for channel in channels:
    for nlayer in nlayers:
        for nnode in nnodes:
            for batchsize in batchsizes:
                for dropout in dropouts:
                    for version in versions:
                        for switch in switches:
                            for analyzer in analyzers:
                                for year in years:
                                    for transform in transforms:
                                        for useLO in useLOs:
                                            name=channel+year+"__"+str(nlayer)+"__"+str(nnode)+"__"+str(batchsize)+"__"+str(dropout)#+"__Trf_"+transform.replace(",","")          
                                            suffix_switch=""
                                            suffix_useLO=""
                                            if switch: suffix_switch="__switch_sig_bkg"
                                            if useLO : suffix_useLO="__useLO"
                                            WORKDIR="WORKDIR"+suffix_useLO+"/"+str(version)+"/"+analyzer+"/"+year+"/"+channel+suffix_switch+"/"+name+"/Trf_"+transform.replace(",","")
                                            command=MakeCommand(WORKDIR,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO)
                                            if nlayers > 30:
                                                memory=10000
                                            else:
                                                memory=False
                                            Export(WORKDIR,command,"dnn_"+channel+"_"+str(version)+"_"+year,submit,1,memory)

