#!/usr/bin/env python
import os
from ExportShellCondorSetup_tamsa import Export
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()
def GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer):
    nlayer=str(nlayer)
    nnode=str(nnode)
    batchsize=str(batchsize)
    dropout=str(dropout)
    version=str(version)
    year=str(year)
    nepoch=str(nepoch)
    ret="--name "+name+" --nlayer "+nlayer+" --nnode "+nnode+" --batchsize "+batchsize+" --dropout "+dropout+" --nepoch "+nepoch+" --version "+version+" --channel "+channel+" --year "+year+" --analyzer "+analyzer
    if switch: ret+=" --switch"
    return ret
def MakeCommand(workdir,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer):
    commandlist=[
        "cd "+curdir,
        "cd "+workdir,
        "python "+maindir+"/script/run_single.py "+GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer),
        ]
    ret="&&".join(commandlist)
    return ret



nlayers=[5,10,20]
#nlayers=[3,4,5,6,7,8]
nnodes=[64,128,256]
#nnodes=[32,48,64,80,96]
batchsizes=[100,1000,3000]
#batchsizes=[50,100,150,200]
dropouts=[0.2,0.3,0.4,0.5]
nepoch=300
#versions=[1.0,1.01,1.02,1.03]
versions=["2405.2"]
#versions=[1.03]
channels=["muon","electron","jet"]
#channels=["electron"]
#channels=["jet"]
#switches=[False,True] ##switch bkg and sig
#switches=[True] 
switches=[False] 
#channels=["electron"]
years=["2016preVFP","2016postVFP","2017","2018"]
analyzers=["EEMu_MuMuE_Method"]
#def Export(WORKDIR,command,jobname,submit,ncpu,memory=False,nretry=3):
submit=True
for nlayer in nlayers:
    for nnode in nnodes:
        for batchsize in batchsizes:
            for dropout in dropouts:
                for channel in channels:
                    for version in versions:
                        for switch in switches:
                            for analyzer in analyzers:
                                for year in years:
                                    name=channel+year+"__"str(nlayer)+"__"+str(nnode)+"__"+str(batchsize)+"__"+str(dropout)

                                    WORKDIR="WORKDIR/"+str(version)+"/"+analyzer+"/"+year+"/"+channel+"/"+name
                                    if switch: WORKDIR="WORKDIR/"+str(version)+"/"+analyzer+"/"+year+"/"+channel+"__switch_sig_bkg/"+name
                                    command=MakeCommand(WORKDIR,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer)
                                    if nlayers > 30:
                                        memory=10000
                                    else:
                                        memory=False
                                    Export(WORKDIR,command,"dnn_"+channel+"_"+str(version)+"_"+year,submit,1,memory)
njobs=len(nlayers)*len(nnodes)*len(batchsizes)*len(dropouts)*len(channels)*len(versions)*len(analyzers)*len(years)
print "njobs=",njobs

'''
usage: run_single.py [-h] [--nlayer NLAYER] [--name NAME] [--nnode NNODE]
                     [--nepoch NEPOCH] [--batchsize BATCHSIZE]
                     [--dropout DROPOUT] [--version VERSION]
                     [--channel CHANNEL]

'''




