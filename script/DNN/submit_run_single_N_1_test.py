#!/usr/bin/env python
from GetCommands import GetOptionCommand,MakeCommand
import os
from ExportShellCondorSetup_tamsa import Export

def GetVariableConfig(version):
        version=str(version)
        exec(open(maindir+"/config/v"+version+"/variables.py"))
        return bmuon_var,belectron_var,bjet_var






maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()


nlayers=[5]
nnodes=[64]
batchsizes=[500]
dropouts=[0.2]
nepoch=300
transforms=["G"]


channels=["muon","electron"]
years=["2016preVFP","2016postVFP","2017","2018"]
analyzers=["EEMu_MuMuE_Method"]

version="2405.4"
bmuonvar,belectronvar,bjetvar=GetVariableConfig(version)


#VarToSkip
submit=1
for channel in channels:
    for nlayer in nlayers:
        for nnode in nnodes:
            for batchsize in batchsizes:
                for dropout in dropouts:
                        for analyzer in analyzers:
                            for year in years:
                                for transform in transforms:
                                        if channel=="muon":
                                                for this_var in bmuonvar+bjetvar:
                                                        this_var_linux=this_var.replace("(","_").replace(")","_").replace("*","_dot_")
                                                        this_var_input=this_var.replace("(","\(").replace(")","\)")
                                                        name=channel+year+"__"+str(nlayer)+"__"+str(nnode)+"__"+str(batchsize)+"__"+str(dropout)
                                                        WORKDIR="WORKDIR__N_1/"+str(version)+"/"+analyzer+"/"+year+"/"+channel+"/"+name+"/Trf_"+transform.replace(",","")+"/No__"+this_var_linux+"/"
                                                        command=MakeCommand(WORKDIR,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,0,year,analyzer,transform,0,this_var_input)
                                                        if nlayers > 30:
                                                                memory=10000
                                                        else:
                                                                memory=False
                                                        Export(WORKDIR,command,"dnn_"+channel+"_"+str(version)+"_"+year,submit,1,memory)

                                        elif channel=="electron":
                                                for this_var in belectronvar+bjetvar:
                                                        this_var_linux=this_var.replace("(","_").replace(")","_").replace("*","_dot_")
                                                        this_var_input=this_var.replace("(","\(").replace(")","\)")
                                                        name=channel+year+"__"+str(nlayer)+"__"+str(nnode)+"__"+str(batchsize)+"__"+str(dropout)
                                                        WORKDIR="WORKDIR__N_1/"+str(version)+"/"+analyzer+"/"+year+"/"+channel+"/"+name+"/Trf_"+transform.replace(",","")+"/No__"+this_var_linux+"/"
                                                        command=MakeCommand(WORKDIR,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,0,year,analyzer,transform,0,this_var_input)
                                                        if nlayers > 30:
                                                                memory=10000
                                                        else:
                                                                memory=False
                                                        Export(WORKDIR,command,"dnn_"+channel+"_"+str(version)+"_"+year,submit,1,memory)
