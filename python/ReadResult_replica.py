import os
import sys
class ReadResult:
    def __init__(self,WORKDIR,version,ana,year,obj,nlayer,nnode,batchsize,dropout,Trf,i):
        self.WORKDIR=WORKDIR
        self.version=str(version)
        self.ana=ana
        self.year=str(year)
        self.obj=obj
        self.nlayer=str(nlayer)
        self.nnode=str(nnode)
        self.batchsize=str(batchsize)
        self.dropout=str(dropout)
        self.Trf=Trf
        self.GetPath(i)
        self.ReadROC()
    def GetPath(self,i):
        #ROC-integ
        #ws/WORKDIR/1.0/muon/10__256__3000__0.5/run.out
        #ws/WORKDIR/2405.2/EEMu_MuMuE_Method/2017/muon/muon2017__10__64__100__0.2/Trf_G
        self.subdirname="__".join([self.obj+self.year,self.nlayer,self.nnode,self.batchsize,self.dropout])
        self.path="/".join([self.WORKDIR,self.version,self.ana,self.year,self.obj,self.subdirname,self.Trf,str(i),"run.out"])
        #print self.path
    def ReadROC(self):
        if not os.path.isfile(self.path) :
            self.roc=0
            return
        f=open(self.path)
        lines=f.readlines()
        readnext=False
        ret=""
        for line in lines:
            #if "ROC-integ" in line : 
            #    readnext=True
            #    continue
            #if readnext:
            #    #print line.split()[4]
            #    ret=line.split()[4]
            #    readnext=False
            if "auc= " in line:
                ret=float(line.replace("auc= ",""))
        f.close()
        if ret=="" : 
            self.roc=0.
        else:
            self.roc=float(ret)
if __name__ == '__main__':
    
    ana="EEMu_MuMuE_Method"
    year=2017
    if len(sys.argv)>1 : year=sys.argv[1]


    version="2405.4.3"
    years=["2016preVFP","2016postVFP","2017","2018"]
    analyzer="EEMu_MuMuE_Method"
    channels={
        "muon":[3,48,1100,0.1,"G"],
        "electron":[3,48,600,0.1,"G"],
        "jet":[5,64,1000,0.2,"G"],
    }
    nepoch=300

    istart=0
    Ntotal=100
    iend=istart+Ntotal


    for channel in channels:
        ana=analyzer
        this_params=channels[channel]
        nlayer=this_params[0]
        nnode=this_params[1]
        batchsize=this_params[2]
        dropout=this_params[3]
        transform=this_params[4]

        min_roc=1.
        best_roc=0.
        best_params=[0,0,0,0,0,""]
        best_i=-1
        for i in range(istart,iend):
            test=ReadResult("/data6/Users/jhchoi/TMVA/TMVA_TOOL/ws/WORKDIR_ntrial",version,ana,year,channel,nlayer,nnode,batchsize,dropout,"Trf_"+transform.replace(",",""),i)
            if test.roc == "" or test.roc==None:continue
            #xprint test.roc
            if float(test.roc) > best_roc:
                best_roc=test.roc
                best_params=[version,nlayer,nnode,batchsize,dropout,transform]
                best_i=i
            if  float(test.roc) < min_roc and float(test.roc)>0.5:
                min_roc=float(test.roc) 
        ##--after find best case
        print "[year]",year
        print "--Best for ", channel,"--"
        print "roc=",best_roc
        print "version,nlayer,nnode,batchsize,dropout,transform"
        print best_params
        print "i=",best_i

        print "--min roc"
        print min_roc
