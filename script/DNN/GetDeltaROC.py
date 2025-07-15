#!/usr/bin/env python
import ROOT

import os
import sys
import glob
def ReadROC(path):
    roc=0
    if not os.path.isfile(path) :
        return roc
    f=open(path)
    lines=f.readlines()
    readnext=False
    ret=""
    for line in lines:
        if "ROC-integ" in line :
            readnext=True
            continue
        if readnext:
            #print line.split()[4]                                                                                                                                                                      
            ret=line.split()[4]
            readnext=False
    f.close()
    if roc=="" : return 0
    roc=float(ret)
    return roc

def GetPath(targetdir,v):
    return targetdir+"/No__"+v+"/run.out"

def GetListOfVariables(targetdir):

    dirlist=glob.glob(targetdir+"/No__*")
    vlist=[]
    for d in dirlist:
        v=d.replace(targetdir,"").replace("/","").replace("No__","")
        vlist.append(v)
    return vlist


if __name__ == '__main__':
    targetdir=sys.argv[1]
    vlist=GetListOfVariables(targetdir)
    for v in vlist:
        path=GetPath(targetdir,v)
        roc=ReadROC(path)
        print v,roc
