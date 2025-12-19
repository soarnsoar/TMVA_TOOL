import os
import pickle
import glob
import sys
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

def GetPerformance(outpath):
    f=open(outpath)
    lines=f.readlines()
    f.close()
    auc=-1
    sigeff_B0p3=-1
    sigeff_B0p1=-1
    sigeff_B0p01=-1
    #auc= 0.7480392378196351
    #sigeff_B0p3
    #BDT_2016preVFP       BDT            : 0.056 (0.071)       0.346 (0.379)      0.673 (0.681)

    sigeff_phrase="overtraining check"
    readsigeff=0
    for line in lines:
        if "auc=" in line :
            auc=float(line.replace("auc=",""))
        if sigeff_phrase in line:
            readsigeff=1
            continue
        if "BDT            : " in line and readsigeff:
            ret=line.split("BDT            :")[1]
            ret=ret.split()
            sigeff_B0p3=[float(ret[4]),float(ret[5].strip("(").strip(")"))]
            sigeff_B0p1=[float(ret[2]),float(ret[3].strip("(").strip(")"))]
            sigeff_B0p01=[float(ret[0]),float(ret[1].strip("(").strip(")"))]

    return auc,sigeff_B0p3,sigeff_B0p1,sigeff_B0p01
def GetRelDiff(a,b):
    ret=0
    if b > 0:
        ret= abs(1-a/b)
        
    #print(ret)
    return ret
def Run(obj):
    print("[",obj,"]")
    years=["2016preVFP","2016postVFP","2017","2018"]
    for year in years:
        print("----------------------",year,"-----------------")
        RunYear(obj,year)
def ParseParamnames(path):
    this_list=path.split('/')
    Trf=this_list[4]
    BoostType=this_list[5]
    #print('this_list[6]=',this_list[6])
    Shrinkage__AdaBoostBeta=""
    if 'Shrinkage__' in this_list[6]: Shrinkage__AdaBoostBeta = this_list[6].split('Shrinkage__')[1]
    if 'AdaBoostBeta__' in this_list[6]:Shrinkage__AdaBoostBeta = this_list[6].split('AdaBoostBeta__')[1]
    NTrees=this_list[7].split('NTrees__')[1]
    MaxDepth=this_list[8].split('MaxDepth__')[1]
    MinNodeSize=this_list[9].split('MinNodeSize__')[1]
    UseBaggedBoost=this_list[10].split('UseBaggedBoost__')[1]
    BaggedSampleFraction=this_list[11].split('BaggedSampleFraction__')[1]
    SeparationType=this_list[12].split('SeparationType__')[1]
    nCuts=this_list[13].split('nCuts__')[1]
    IgnoreNegWeightsInTraining=this_list[14].split('IgnoreNegWeightsInTraining__')[1]
    return Trf,BoostType,Shrinkage__AdaBoostBeta,NTrees,MaxDepth,MinNodeSize,UseBaggedBoost,BaggedSampleFraction,SeparationType,nCuts,IgnoreNegWeightsInTraining
def RunYear(obj,Year,transform):
    ret=[]
    jobname=obj+"__"+str(Year)+"__"+transform
    year=Year
    #obj="electron"
    Trf=transform
    #overfit_threshold=0.03
    overfit_threshold=1. ## reldiff must be less than this value
    outlist=glob.glob("WORKDIR/2409.2/"+year+"/"+obj+"/"+Trf+"/*/*/NTrees__*/MaxDepth__*/MinNodeSize__*/UseBaggedBoost*/BaggedSampleFraction*/SeparationType__*/nCuts__*/IgnoreNegWeightsInTraining__*/run.out")
    print(len(outlist))
    maxauc=-1
    maxauc_info={}
    maxeff=-1
    maxeff_info={}
    
    nFail=0
    print('len(outlist)=',len(outlist))
    all_outinfo={}
    nscan=0
    for out in outlist:
        Trf,BoostType,Shrinkage__AdaBoostBeta,NTrees,MaxDepth,MinNodeSize,UseBaggedBoost,BaggedSampleFraction,SeparationType,nCuts,IgnoreNegWeightsInTraining=ParseParamnames(out)
        
        #print(out)
        auc,sigeff_B0p3,sigeff_B0p1,sigeff_B0p01=GetPerformance(out)
        all_outinfo[out]={
            "auc":auc,
            "sigeff_B0p3":sigeff_B0p3,
            "sigeff_B0p1":sigeff_B0p1,
            "sigeff_B0p01":sigeff_B0p01,
            }
        if auc < 0 :
            nFail+=1
            continue
        if auc < 0.55 : continue
        this_ret={
            "Trf":Trf,
            "BoostType":BoostType,
            "Shrinkage__AdaBoostBeta":Shrinkage__AdaBoostBeta,
            "NTrees":NTrees,
            "MaxDepth":MaxDepth,
            "MinNodeSize":MinNodeSize,
            "UseBaggedBoost":UseBaggedBoost,
            "BaggedSampleFraction":BaggedSampleFraction,
            "SeparationType":SeparationType,
            "nCuts":nCuts,
            "IgnoreNegWeightsInTraining":IgnoreNegWeightsInTraining,
            "auc":auc,
            "sigeff_B0p3":sigeff_B0p3+[],
            "sigeff_B0p1":sigeff_B0p1+[],
            "sigeff_B0p01":sigeff_B0p01+[],
        }
        ret.append(this_ret)
        nscan+=1
        #print(nscan)
        ##for test
        #if nscan>100:
        #    break
    os.system('mkdir -p pickles/')
    with open('pickles/'+jobname+".pkl", "wb") as f:
        pickle.dump(ret, f)
    del ret

    
            
import sys
this_obj=sys.argv[1]
this_year=sys.argv[2]
this_transform=sys.argv[3]
RunYear(this_obj,this_year,this_transform)

#Run("muon")    
#Run("electron")
#Run("jet")
#RunYear("muon","2016postVFP")
#RunYear("muon","2018")
#RunYear("muon","2016preVFP")
#RunYear("jet","2016preVFP")
#RunYear("jet","2016postVFP")    
