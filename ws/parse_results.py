import glob
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
def RunYear(obj,Year):
    year=Year
    #obj="electron"
    Trf="*"
    overfit_threshold=0.5
    outlist=glob.glob("WORKDIR/2409.2/"+year+"/"+obj+"/"+Trf+"/*/*/NTrees__*/MaxDepth__*/MinNodeSize__*/UseBaggedBoost*/BaggedSampleFraction*/SeparationType__*/nCuts__*/IgnoreNegWeightsInTraining__*/run.out")
    print(len(outlist))
    maxauc=-1
    maxauc_info={}
    maxeff=-1
    maxeff_info={}
    
    nFail=0

    all_outinfo={}
    
    for out in outlist:
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
        if GetRelDiff(sigeff_B0p3[0],sigeff_B0p3[1]) > overfit_threshold : continue
        #if GetRelDiff(sigeff_B0p1[0],sigeff_B0p1[1]) > overfit_threshold : continue
        #if GetRelDiff(sigeff_B0p01[0],sigeff_B0p01[1]) > overfit_threshold : continue
        if auc > maxauc:
            maxauc_info["path"]=out
            maxauc_info["auc"]=auc
            maxauc_info["sigeff"]=sigeff_B0p3
            maxauc=auc
        if sigeff_B0p3[0] > maxeff:
            maxeff_info["path"]=out
            maxeff_info["auc"]=auc
            maxeff_info["sigeff"]=sigeff_B0p3
            maxeff=sigeff_B0p3[0]

    
            
    print("[maxauc]")
    print(maxauc_info)
    print("[maxeff]")
    print(maxeff_info)
    
    print("nFail=",nFail)
    ##---Find Similar Performance
    print ("##---Similar Perf--##")
    for out in all_outinfo:
        this_auc=all_outinfo[out]['auc']
        if (maxauc-this_auc)/maxauc < 0.01:
            print(this_auc,out)

Run("muon")    
Run("electron")
Run("jet")
