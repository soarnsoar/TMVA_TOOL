#!/usr/bin/env python
from GetCommands import GetOptionCommand,MakeCommand
import os
from ExportShellCondorSetup_tamsa import Export
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()

##---v2405.4.3
version="2405.4.3"
years=["2016preVFP","2016postVFP","2017","2018"]
analyzer="EEMu_MuMuE_Method"
channels={
    "muon":[3,48,1100,0.1,"G"],
    "electron":[3,48,600,0.1,"G"],
    "jet":[5,64,1000,0.2,"G"],
}
nepoch=300

submit=1
istart=100
Ntotal=100
iend=istart+Ntotal
for year in years:
    for channel in channels:
        for i in range(istart,iend):
            this_params=channels[channel]
            nlayer=this_params[0]
            nnode=this_params[1]
            batchsize=this_params[2]
            dropout=this_params[3]
            transform=this_params[4]
            name=channel+year+"__"+str(nlayer)+"__"+str(nnode)+"__"+str(batchsize)+"__"+str(dropout)#+"__Trf_"+transform.replace(",","")          
            WORKDIR="WORKDIR_ntrial/"+str(version)+"/"+analyzer+"/"+year+"/"+channel+"/"+name+"/Trf_"+transform.replace(",","")+"/"+str(i)
            command=MakeCommand(WORKDIR,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,0,year,analyzer,transform,0)
            memory=False
            Export(WORKDIR,command,"dnn_"+channel+"_"+str(version)+"_"+year,submit,1,memory)
