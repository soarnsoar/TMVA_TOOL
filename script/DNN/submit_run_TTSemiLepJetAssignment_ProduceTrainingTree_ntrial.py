#!/usr/bin/env python
from GetCommands import GetOptionCommand,MakeCommand
import os
from ExportShellCondorSetup_tamsa import Export



maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()
def GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,year,analyzer,transform,flag):
    nlayer=str(nlayer)
    nnode=str(nnode)
    batchsize=str(batchsize)
    dropout=str(dropout)
    version=str(version)
    year=str(year)
    nepoch=str(nepoch)
    ret="--name "+name+" --nlayer "+nlayer+" --nnode "+nnode+" --batchsize "+batchsize+" --dropout "+dropout+" --nepoch "+nepoch+" --version "+version+" --year "+year+" --analyzer "+analyzer+" --transform "+transform+" --flag "+flag
    return ret
def MakeCommand(workdir,name,nlayer,nnode,batchsize,dropout,nepoch,version,year,analyzer,transform,flag):
    commandlist=[
        "cd "+curdir,
        "cd "+workdir,
        "python "+maindir+"/script/run_TTSemiLepJetAssignment_ProduceTrainingTree.py "+GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,year,analyzer,transform,flag),
        ]
    ret="&&".join(commandlist)
    return ret



##---1st
nlayers=[5]
nnodes=[128]
batchsizes=[500]
dropouts=[0.2]
nepoch=300
transforms=["G"]
versions=["1.0"]
#years=["2016preVFP","2016postVFP","2017","2018"]
years=["2016preVFP","2016postVFP"]
analyzers=["TTSemiLepJetAssignment_ProduceTrainingTree"]




submit=1
flag="reduction_1M__"
ntrial=75
for nlayer in nlayers:
    for nnode in nnodes:
        for batchsize in batchsizes:
            for dropout in dropouts:
                for version in versions:
                    for analyzer in analyzers:
                        for year in years:
                            for transform in transforms:
                                for n in range(ntrial):
                                    name=year+"__"+str(nlayer)+"__"+str(nnode)+"__"+str(batchsize)+"__"+str(dropout)#+"__Trf_"+transform.replace(",","")          
                                    WORKDIR="WORKDIR_TTSemiLepJetAssignment_ntrial/"+str(version)+"/"+analyzer+"/"+year+"/"+name+"/Trf_"+transform.replace(",","")+"/"+str(n)
                                    command=MakeCommand(WORKDIR,name,nlayer,nnode,batchsize,dropout,nepoch,version,year,analyzer,transform,flag)
                                    if nlayers > 30:
                                        memory=10000
                                    else:
                                        memory=False
                                    Export(WORKDIR,command,"dnn_TTSemiLepJetAssignment_"+str(version)+"_"+year+"__ntrial",submit,1,memory)

