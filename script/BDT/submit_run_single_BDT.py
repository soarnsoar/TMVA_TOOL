#!/usr/bin/env python
from GetCommands import GetOptionCommand,MakeCommand
import os
from ExportShellCondorSetup_tamsa import Export
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()

curdir=os.getcwd()
def GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO,VarToSkip=None):
    nlayer=str(nlayer)
    nnode=str(nnode)
    batchsize=str(batchsize)
    dropout=str(dropout)
    version=str(version)
    year=str(year)
    nepoch=str(nepoch)
    ret="--name "+name+" --nlayer "+nlayer+" --nnode "+nnode+" --batchsize "+batchsize+" --dropout "+dropout+" --nepoch "+nepoch+" --version "+version+" --channel "+channel+" --year "+year+" --analyzer "+analyzer+" --transform "+transform
    if VarToSkip: ret+=" --VarToSkip "+VarToSkip
    return ret

def MakeCommand(workdir,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO,VarToSkip=None):
    commandlist=[
        "cd "+curdir,
        "cd "+workdir,
        "python "+maindir+"/script/run_single.py "+GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO,VarToSkip),
        ]
    ret="&&".join(commandlist)
    return ret



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
channels=["muon","electron","jet"]


submit=False
for channel in channels:
    for version in versions:
        for analyzer in analyzers:
            for year in years:
                for transform in transforms:
                
                    name=channel+year+"__"+str(nlayer)+"__"+str(nnode)+"__"+str(batchsize)+"__"+str(dropout)#+"__Trf_"+transform.replace(",","")          

                    WORKDIR="WORKDIR"+"/"+str(version)+"/"+analyzer+"/"+year+"/"+channel+"/"+name+"/Trf_"+transform.replace(",","")
                    command=MakeCommand(WORKDIR,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,year,analyzer,transform,useLO)
                    if nlayers > 30:
                        memory=10000
                    else:
                        memory=False
                    Export(WORKDIR,command,"BDT_"+channel+"_"+str(version)+"_"+year,submit,1,memory)

