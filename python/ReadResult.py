import os
class ReadResult:
    def __init__(self,WORKDIR,version,obj,nlayer,nnode,batchsize,dropout):
        self.WORKDIR=WORKDIR
        self.version=str(version)
        self.obj=obj
        self.nlayer=str(nlayer)
        self.nnode=str(nnode)
        self.batchsize=str(batchsize)
        self.dropout=str(dropout)
        self.GetPath()
        self.ReadROC()
    def GetPath(self):
        #ROC-integ
        #ws/WORKDIR/1.0/muon/10__256__3000__0.5/run.out
        self.subdirname="__".join([self.nlayer,self.nnode,self.batchsize,self.dropout])
        self.path="/".join([self.WORKDIR,self.version,self.obj,self.subdirname,"run.out"])
        
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
        self.roc=ret
if __name__ == '__main__':
    #test=ReadResult("/data6/Users/jhchoi/TMVA/TMVA_TOOL/ws/WORKDIR",1.0,"muon",10,256,3000,0.5)
    ##--1st
    #    nlayers=[5,10,20,40,80]
    nlayers=[5,10,20]
    nnodes=[64,128,256]#[64,128,256]
    batchsizes=[100,1000,3000]
    dropouts=[0.2,0.5]
    nepoch=300
    #versions=[1.0,1.01,1.02,1.03]
    versions=["2405.2"]
    channels=["muon","electron","jet"]
    #isSwitch=True
    isSwitch=False


    for channel in channels:
        if isSwitch: channel+="__switch_sig_bkg"
        best_roc=0
        best_params=[0,0,0,0,0]
        for version in versions:
            for nlayer in nlayers:
                for nnode in nnodes:
                    for batchsize in batchsizes:
                        for dropout in dropouts:

                            test=ReadResult("/data6/Users/jhchoi/TMVA/TMVA_TOOL/ws/v"+version+"/WORKDIR",version,channel,nlayer,nnode,batchsize,dropout)
                            if test.roc == "" or test.roc==None:continue
                            if float(test.roc) > best_roc:
                                best_roc=test.roc
                                best_params=[version,nlayer,nnode,batchsize,dropout]
        ##
        ##--after find best case
        print "--Best for ", channel,"--"
        print "roc=",best_roc
        print "version,nlayer,nnode,batchsize,dropout"
        print best_params
                            
