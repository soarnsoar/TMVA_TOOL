#!/usr/bin/env python
import os
from ExportShellCondorSetup_tamsa import Export
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()
def GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO):
    nlayer=str(nlayer)
    nnode=str(nnode)
    batchsize=str(batchsize)
    dropout=str(dropout)
    version=str(version)
    year=str(year)
    nepoch=str(nepoch)
    ret="--name "+name+" --nlayer "+nlayer+" --nnode "+nnode+" --batchsize "+batchsize+" --dropout "+dropout+" --nepoch "+nepoch+" --version "+version+" --channel "+channel+" --year "+year+" --analyzer "+analyzer+" --transform "+transform
    if switch: ret+=" --switch"
    if useLO: ret+=" --useLO"
    return ret
def MakeCommand(workdir,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO):
    commandlist=[
        "cd "+curdir,
        "cd "+workdir,
        "python "+maindir+"/script/run_single.py "+GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO),
        ]
    ret="&&".join(commandlist)
    return ret



nlayers=[5]
#nlayers=[3,4,5,6,7,8]
nnodes=[64]
#nnodes=[32,48,64,80,96]
batchsizes=[100]
#batchsizes=[50,100,150,200]
dropouts=[0.2]
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
transforms=["I","N,D","G","U","P","N"]
transforms=["N"]
useLOs=[True, False]

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
                                            Export(WORKDIR,command,"dnn_VarTrsfTest_"+channel+"_"+str(version)+"_"+year,submit,1,memory)
njobs=len(nlayers)*len(nnodes)*len(batchsizes)*len(dropouts)*len(channels)*len(versions)*len(analyzers)*len(years)
print "njobs=",njobs

'''
usage: run_single.py [-h] [--nlayer NLAYER] [--name NAME] [--nnode NNODE]
                     [--nepoch NEPOCH] [--batchsize BATCHSIZE]
                     [--dropout DROPOUT] [--version VERSION]
                     [--channel CHANNEL]

'''




