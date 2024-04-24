#!/usr/bin/env python
import os
from ExportShellCondorSetup_tamsa import Export

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
        "run_single.py "+GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel),
        ]
    ret="&&".join(commandlist)
    return ret



nlayers=[5,10,20,40,80]
nnodes=[64,128,256]
batchsizes=[100,1000,3000]
dropouts=[0.2,0.5]
nepoch=300
version=1.0
channels=["muon","electron","jet"]

#def Export(WORKDIR,command,jobname,submit,ncpu,memory=False,nretry=3):

for nlayer in nlayers:
    for nnode in nnodes:
        for batchsize in batchsizes:
            for dropout in dropouts:
                for channel in channels:
                    name=str(nlayer)+"__"+str(nnode)+"__"+str(batchsize)+"__"+str(dropout)
                    WORKDIR="WORKDIR/"+channel+"/"+name
                    command=MakeCommand(WORKDIR,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel)
                    Export(WORKDIR,command,"dnn_"+channel,1,1)
njobs=len(nlayers)*len(nnodes)*len(batchsizes)*len(dropouts)*len(channels)
print "njobs=",njobs

'''
usage: run_single.py [-h] [--nlayer NLAYER] [--name NAME] [--nnode NNODE]
                     [--nepoch NEPOCH] [--batchsize BATCHSIZE]
                     [--dropout DROPOUT] [--version VERSION]
                     [--channel CHANNEL]

'''




