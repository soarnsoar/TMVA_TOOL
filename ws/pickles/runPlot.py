import os
import pickle
import ROOT
import glob
ROOT.gROOT.SetBatch(True)
def GetRelDiff(v1,v2):
    if v2 <= 0 : return 1
    return abs(1-v1/v2)
# Trf,BoostType,Shrinkage__AdaBoostBeta,NTrees,MaxDepth,MinNodeSize,UseBaggedBoost,BaggedSampleFraction,SeparationType,nCuts,IgnoreNegWeightsInTraining

dict_bound={
    "Shrinkage__AdaBoostBeta":[0.005, 0.2],
    "NTrees":[100, 2000],
    "MaxDepth":[1,6],
    "BaggedSampleFraction":[0.1,1.1],
    "MinNodeSize":[0.1,15],
    "nCuts":[5,50],
}


def IsWithinBoundary(_r):
    ##r = result
    for key in ["Shrinkage__AdaBoostBeta","NTrees","MaxDepth","MinNodeSize","BaggedSampleFraction","nCuts"]:
        this_value=float(_r[key])
        if key=="BaggedSampleFraction":
            #print(this_value)
            if this_value== 0. : return 1
        if this_value < dict_bound[key][0] : return 0
        if this_value > dict_bound[key][1] : return 0            
    return 1


class Plotter:
    def __init__(self,name,result,key1,key2):
        self.name=name
        self.result=result
        self.key1=key1
        self.key2=key2
        
        self.list_v1=self.CheckPossibleValue(key1)
        self.list_v2=self.CheckPossibleValue(key2)

        self.dict_bound={
            "Shrinkage__AdaBoostBeta":[0.005, 1],
            "NTrees":[100, 2000],
            "MaxDepth":[1,6],
            "BaggedSampleFraction":[0.1,1],
            "MinNodeSize":[0.1,5],
            "nCuts":[5,50],
        }

        #self.DrawGraph()
    def CheckPossibleValue(self,key):
        possible_values = set(r[key] for r in self.result)
        mylist=list(possible_values)
        newlist=[]
        for v in mylist:
            newlist.append(float(v))
        newlist=sorted(newlist)
        return newlist              
    
        
        
    def GetBestAUCForGivenPair(self,value1,value2,overfit_threshold=0.1):
        filtered = [r for r in self.result if float(r[self.key1])==value1 and float(r[self.key2])==value2 and GetRelDiff(r['sigeff_B0p3'][0],r['sigeff_B0p3'][1])<0.1 and GetRelDiff(r['sigeff_B0p1'][0],r['sigeff_B0p1'][1])<0.1 and GetRelDiff(r['sigeff_B0p01'][0],r['sigeff_B0p01'][1])<0.2 and IsWithinBoundary(r)]
        if len(filtered) == 0 :return 0
        best = max(filtered, key=lambda r: r['auc'])
        return best['auc']

    def DrawGraph(self):
        print("<DrawGraph>",self.key1,self.key2)
        best_auc=-1
        best_v1=-1
        best_v2=-1
        self.graph = ROOT.TGraph2D()
        keyname1=self.key1.replace("__AdaBoostBeta","")
        keyname2=self.key2.replace("__AdaBoostBeta","")
        self.graph.SetTitle(keyname1+":"+keyname2)
        k=0
        for v1 in self.list_v1:
            for v2 in self.list_v2:
                this_auc=self.GetBestAUCForGivenPair(v1,v2)
                if this_auc<0.5 :
                    #this_auc=0.5
                    continue ##skip
                ##BaggedSampleFraction
                if keyname1=="BaggedSampleFraction" and v1==0 : v1=1
                if keyname2=="BaggedSampleFraction" and v2==0 : v2=1
                self.graph.SetPoint(k,v1,v2,this_auc)
                k+=1
                if this_auc > best_auc:
                    best_auc=this_auc
                    best_v1=v1
                    best_v2=v2
        print('Number of points in graph=',k)
        if k <3 : self.graph.SetPoint(k,0,0,0)
        c=ROOT.TCanvas("","",800,600)
        self.graph.Draw("COLZ")
        ##---draw best auc point---##
        pm = ROOT.TGraph()
        pm.SetPoint(0, best_v1, best_v2)
        pm.SetMarkerStyle(5)
        pm.SetMarkerSize(2.0)
        pm.SetMarkerColor(ROOT.kBlack)
        pm.Draw("Psame")


        
        os.system('mkdir -p plots/'+self.name+"/")
        c.SaveAs('plots/'+self.name +"/" +  "__".join([self.name,keyname1,keyname2]) +".pdf")
        c.SetLogz()
        c.SaveAs('plots/'+self.name +"/logz__" +  "__".join([self.name,keyname1,keyname2]) +".pdf")

        print('-----------')
        print(keyname1,'=',best_v1)
        print(keyname2,'=',best_v2)
        print('best_auc=',best_auc)

def GetBestPoint(result):
    _filtered = [r for r in result if GetRelDiff(r['sigeff_B0p3'][0],r['sigeff_B0p3'][1])<0.1 and GetRelDiff(r['sigeff_B0p1'][0],r['sigeff_B0p1'][1])<0.1 and GetRelDiff(r['sigeff_B0p01'][0],r['sigeff_B0p01'][1])<0.2 and IsWithinBoundary(r)]
    if len(_filtered) == 0 :return 0
    best = max(_filtered, key=lambda r: r['auc'])
    print(best)        
#jet2016postVFP/run.done  jet2016preVFP/run.done  jet2017/run.done  jet2018/run.done  muon2016postVFP/run.done  muon2016preVFP/run.done
import sys
obj=sys.argv[1]
year=sys.argv[2]
#obj='jet'
#year='2016postVFP'



#list_Shrinkage=['0.04', '0.06','0.08','0.12']
#list_NTrees=['500', '600','700','800']
#list_MaxDepth=['4','5','6']
#list_BaggedSampleFraction=['0.4', '0.5', '0.6','0.7']
#list_MinNodeSize=['1.0','2.5']
#list_nCuts=['10','20','30']

JetKeyList={
    'Shrinkage__AdaBoostBeta':[0.04,0.06,0.08,0.12],
    'NTrees':[500,600,700,800],
    'MaxDepth':[4,5,6],
    'BaggedSampleFraction':[0,0.4,0.5,0.6,0.7],
    'MinNodeSize':[1,2.5],
    'nCuts':[10,20,30]
}
JetKeyList={}
LeptonKeyList={
    'Shrinkage__AdaBoostBeta':[0.0001,0.001,0.003,0.005,0.007,0.01,0.05, 0.07,0.1,0.15,0.2],
    'NTrees':[500, 600,700,800, 1200],
    'MaxDepth':[4,5,6],
    'BaggedSampleFraction':[0,0.2,0.3,0.4, 0.5, 0.6,0.7],
    'MinNodeSize':[1.0,1.5,2.0,2.5,3.0],
    'nCuts':[10,20,30,40]

}
LeptonKeyList={}

####
search=obj+"__"+year+"*.pkl"
pkls=glob.glob(search)
result=[]
for path in pkls:
    #path='old/'+obj+"__"+year+".pkl"
    with open(path,"rb") as f:
        this_result = pickle.load(f)        
        this_result = [r for r in this_result if r['BoostType'] == 'Grad']
        result+=this_result
    print('---',path,'----')
print('nresult=',len(result))
GetBestPoint(result)    
#Shrinkage__AdaBoostBeta,NTrees,MaxDepth,MinNodeSize,UseBaggedBoost,BaggedSampleFraction,SeparationType,nCuts
keylist=["Shrinkage__AdaBoostBeta","NTrees","MaxDepth","MinNodeSize","BaggedSampleFraction","nCuts"]
for i1,key1 in enumerate(keylist):
    for i2,key2 in enumerate(keylist):
        if i1<=i2 : continue
        myplot=Plotter(obj+"__"+year,result,key1,key2)
        if obj=='jet':
            if key1 in JetKeyList : myplot.list_v1=JetKeyList[key1]
            if key2 in JetKeyList : myplot.list_v2=JetKeyList[key2]
        else:
            if key1 in LeptonKeyList : myplot.list_v1=LeptonKeyList[key1]
            if key2 in LeptonKeyList : myplot.list_v2=LeptonKeyList[key2]                
        myplot.DrawGraph()
        del myplot
