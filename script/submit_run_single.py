#!/usr/bin/env python
import os
from ExportShellCondorSetup_tamsa import Export
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()
def GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel):
    nlayer=str(nlayer)
    nnode=str(nnode)
    batchsize=str(batchsize)
    dropout=str(dropout)
    version=str(version)
    ret="--name "+name+" --nlayer "+nlayer+" --nnode "+nnode+" --batchsize "+batchsize+" --dropout "+dropout+" --version "+version+" --channel "+channel
    return ret
def MakeCommand(workdir,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel):
    commandlist=[
        "cd "+curdir,
        "cd "+workdir,
        "python "+maindir+"/script/run_single.py "+GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel),
        ]
    ret="&&".join(commandlist)
    return ret



nlayers=[5,10,20,40,80]
nnodes=[64,128,256]
batchsizes=[100,1000,3000]
dropouts=[0.2,0.5]
nepoch=300
versions=[1.0,1.01,1.02,1.03]
#versions=[1.0]
#versions=[1.03]
channels=["muon","electron","jet"]

#def Export(WORKDIR,command,jobname,submit,ncpu,memory=False,nretry=3):

for nlayer in nlayers:
    for nnode in nnodes:
        for batchsize in batchsizes:
            for dropout in dropouts:
                for channel in channels:
                    for version in versions:
                        name=str(nlayer)+"__"+str(nnode)+"__"+str(batchsize)+"__"+str(dropout)
                        WORKDIR="WORKDIR/"+str(version)+"/"+channel+"/"+name
                        command=MakeCommand(WORKDIR,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel)
                        if nlayers > 30:
                            memory=10000
                        else:
                            memory=False
                        Export(WORKDIR,command,"dnn_"+channel+"_"+str(version),1,1,memory)
njobs=len(nlayers)*len(nnodes)*len(batchsizes)*len(dropouts)*len(channels)*len(versions)
print "njobs=",njobs

'''
usage: run_single.py [-h] [--nlayer NLAYER] [--name NAME] [--nnode NNODE]
                     [--nepoch NEPOCH] [--batchsize BATCHSIZE]
                     [--dropout DROPOUT] [--version VERSION]
                     [--channel CHANNEL]

'''




