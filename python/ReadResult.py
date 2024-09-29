import os
import sys
class ReadResult:
    def __init__(self,WORKDIR,version,ana,year,obj,nlayer,nnode,batchsize,dropout,Trf):
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
        self.GetPath()
        self.ReadROC()
    def GetPath(self):
        #ROC-integ
        #ws/WORKDIR/1.0/muon/10__256__3000__0.5/run.out
        #ws/WORKDIR/2405.2/EEMu_MuMuE_Method/2017/muon/muon2017__10__64__100__0.2/Trf_G
        self.subdirname="__".join([self.obj+self.year,self.nlayer,self.nnode,self.batchsize,self.dropout])
        self.path="/".join([self.WORKDIR,self.version,self.ana,self.year,self.obj,self.subdirname,self.Trf,"run.out"])
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
            if "ROC-integ" in line : 
                readnext=True
                continue
            if readnext:
                #print line.split()[4]
                ret=line.split()[4]
                readnext=False
        f.close()
        if ret=="" : 
            self.roc=0.
        else:
            self.roc=float(ret)
if __name__ == '__main__':
    #test=ReadResult("/data6/Users/jhchoi/TMVA/TMVA_TOOL/ws/WORKDIR",1.0,"muon",10,256,3000,0.5)
    ##--1st
    #nlayers=[5,10,20,40,80]
    #nlayers=[5,10,20]
    #nnodes=[64,128,256]#[64,128,256]
    #batchsizes=[100,1000,3000]
    #dropouts=[0.2,0.5]
    
    ana="EEMu_MuMuE_Method"
    year="2016preVFP"
    if len(sys.argv)>1 : year=sys.argv[1]

    ##---1st





    channels=["muon","electron","jet"]
    switches=[False]
    useLOs=[False]


    nlayers=[5,10,20]
    nnodes=[64,128,256]
    batchsizes=[100,500,1000]
    dropouts=[0.2,0.4,0.6]

    nepoch=300
    #versions=[1.0,1.01,1.02,1.03]
    #versions=["2405.4","2405.4_jc"]
    ##2409.1
    versions=["2409.1"]
    channels=["muon","electron","jet"]
    #channels=["muon","electron"]
    transforms=["I","G","U","P","N"]
    #useLOs=[True, False]
    useLOs=[False]

    #isSwitch=True
    isSwitch=False



    ##--2nd
    #nlayers=[1,2,3,4,5,6,7]
    #nnodes=[50,64,80]
    #batchsizes=[90,100,110,120]
    #dropouts=[0.1,0.2,0.3]
    #nepoch=300
    #transforms=["I","I,N","N,U","N"]+["G","G,U","N,G","N,G,U","N,U,G"]
    #useLOs=[False]

    for channel in channels:
        best_roc=0.
        best_params=[0,0,0,0,0,""]
        if isSwitch: channel+="__switch_sig_bkg"
        for useLO in useLOs:
            suffixLO=""
            if useLO:suffixLO="__useLO"

            for version in versions:

                for nlayer in nlayers:
                    for nnode in nnodes:
                        for batchsize in batchsizes:
                            for dropout in dropouts:
                                for transform in transforms:
                                    test=ReadResult("/data6/Users/jhchoi/TMVA/TMVA_TOOL/ws/WORKDIR"+suffixLO,version,ana,year,channel,nlayer,nnode,batchsize,dropout,"Trf_"+transform.replace(",",""))
                                    if test.roc == "" or test.roc==None:continue

                                    if float(test.roc) > best_roc:
                                        best_roc=test.roc
                                        best_params=[version,nlayer,nnode,batchsize,dropout,transform]

        ##--after find best case
        print "[year]",year
        print "--Best for ", channel,"--"
        print "roc=",best_roc
        print "version,nlayer,nnode,batchsize,dropout,transform"
        print best_params
                            
