#!/usr/bin/env python
from ReadResult import ReadResult
import sys
import os
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
#/data6/Users/jhchoi/TMVA/TMVA_TOOL/ws/WORKDIR
#    def __init__(self,WORKDIR,version,ana,year,obj,nlayer,nnode,batchsize,dropout,Trf):
workdir=maindir+"/ws/WORKDIR/"
year=sys.argv[1]
ana="EEMu_MuMuE_Method"
version=sys.argv[2]
nlayer=sys.argv[3]
nnode=sys.argv[4]
batchsize=sys.argv[5]
dropout=sys.argv[6]
Trf="Trf_"+sys.argv[7].replace(",","")

print year
for obj in ["muon","electron"]:
    print "---"
    print obj
    test=ReadResult(workdir,version,ana,year,obj,nlayer,nnode,batchsize,dropout,Trf)
    print test.roc



