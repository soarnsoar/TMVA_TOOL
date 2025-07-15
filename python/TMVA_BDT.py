import ROOT
import os



class TMVA_TOOL:
    def __init__(self):
        self.dict_tree={}
        self.methodlist=[]
        ##--Set Default setup
        self.SetFactoryName("TMVAClassification")
        self.SetFactoryOption(
            ":".join(["!V",
                      "!Silent",
                      "Color",
                      "DrawProgressBar",
                      "Transformations=I",
                      "AnalysisType=Classification",
                  ])
        )

        self.AddMethod(    {
            'type' : ROOT.TMVA.Types.kBDT,
            'name' : "BDT",
            'options' : ":".join([
                "!H",
                "!V",
                "NTrees=__NTrees__",
                "MinNodeSize=__MinNodeSize__%",
                "MaxDepth=__MaxDepth__",
                "BoostType=__BoostType__",
                "AdaBoostBeta=__AdaBoostBeta__",
                "UseBaggedBoost=__UseBaggedBoost__",
                "BaggedSampleFraction=__BaggedSampleFraction__",
                "SeparationType=__SeparationType__",
                "nCuts=__nCuts__",
                "IgnoreNegWeightsInTraining=__IgnoreNegWeightsInTraining__",
            ])
            
        }
                       )
        self.SetDataOption("!V")
        self.dict_AUC={}
    def SetInputVariables(self,_variables):
        self.variables=_variables
        self.input_dim=len(self.variables)
    def SetSpectators(self,_spectators):
        self.spectators=_spectators
    def SetCut_Sig(self,cut_exp):
        print("<sig cut>=",cut_exp)
        self.cut_sig=cut_exp
    def SetCut_Bkg(self,cut_exp):
        print("<bkg cut>=",cut_exp)
        self.cut_bkg=cut_exp

    def SetFactoryName(self,factoryname):
        self.factoryname=factoryname
    def SetFactoryOption(self,factoryoption):
        self.factoryoption=factoryoption
    def SetTestTreeAndInput_Sig(self,testtree,inputlist):
        self.testtree_sig=testtree
        self.testinputlist_sig=inputlist
    def SetTestTreeAndInput_Bkg(self,testtree,inputlist):
        self.testtree_bkg=testtree
        self.testinputlist_bkg=inputlist
    def SetTrainTreeAndInput_Sig(self,traintree,inputlist):
        self.traintree_sig=traintree
        self.traininputlist_sig=inputlist
    def SetTrainTreeAndInput_Bkg(self,traintree,inputlist):
        self.traintree_bkg=traintree
        self.traininputlist_bkg=inputlist

    def SetWeight_Sig(self,exp):
        self.weight_exp_sig=exp
    def SetWeight_Bkg(self,exp):
        self.weight_exp_bkg=exp
    def SetDataOption(self,_option):
        self.dataoption=_option
    def SetTransform(self,transform):
        self.transform=transform
    ###---BDT Params
    def SetNTrees(self,NTrees):
        self.NTrees=NTrees
    def SetMaxDepth(self,MaxDepth):
        self.MaxDepth=MaxDepth
    def SetShrinkage(self,Shrinkage):
        self.Shrinkage=Shrinkage
    def SetMinNodeSize(self,MinNodeSize):
        self.MinNodeSize=MinNodeSize
    def SetBoostType(self,BoostType):
        self.BoostType=BoostType
    def SetAdaBoostBeta(self,AdaBoostBeta):
        self.AdaBoostBeta=AdaBoostBeta        
    def SetUseBaggedBoost(self,UseBaggedBoost):
        self.UseBaggedBoost=UseBaggedBoost
    def SetBaggedSampleFraction(self,BaggedSampleFraction):
        self.BaggedSampleFraction=BaggedSampleFraction
    def SetSeparationType(self,SeparationType):
        self.SeparationType=SeparationType
    def SetnCuts(self,nCuts):
        self.nCuts=nCuts
    def SetIgnoreNegWeightsInTraining(self,IgnoreNegWeightsInTraining):
        self.IgnoreNegWeightsInTraining=IgnoreNegWeightsInTraining
    ###---[END] BDT Params
    def AddMethod(self,_method):
        self.methodlist.append(_method)
    def SetOutputName(self,outputname):
        self.outputname=outputname
    def Run(self):
        self.InitTMVA()
        self.SetTreeInfo()
        self.SetFactory()
        self.RunTrain()
    def RunTrain(self):
        print("self.factory.TrainAllMethods")
        self.factory.TrainAllMethods()
        print("[END]self.factory.TrainAllMethods")
        print("self.factory.TestAllMethods")
        self.factory.TestAllMethods()
        print("[END]self.factory.TestAllMethods")
        print("self.factory.EvaluateAllMethods")
        self.factory.EvaluateAllMethods()
        print("[END]self.factory.EvaluateAllMethods")
        print("method ref cut and auc")
        for method in self.methodlist:
            _cut=self.factory.GetMethod(self.factoryname,method['name']).GetSignalReferenceCut()
            _auc=self.factory.GetROCIntegral(self.dataloader,method['name'])
            print("ref.cut=",method['name'],_cut)
            print("auc=",_auc)
            self.dict_AUC[method['name']]=_auc
            #_sigeff=self.factory.GetMethod(self.factoryname,method['name']).GetEfficiency(_cut,"SigEff")
            #print "sig.eff=",_sigeff
            #_bkgeff=self.factory.GetMethod(self.factoryname,method['name']).GetEfficiency(_cut,"BkgEff")
            #print "bkg.eff=",_sigeff
        print ("self.fout.Close")
        self.fout.Close()
        print ("[END]self.fout.Close")
    def GetAUC(self,_name):
        return self.dict_AUC[_name]
    def SetFactory(self):
        self.fout = ROOT.TFile(self.outputname,"RECREATE")
        self.factory=ROOT.TMVA.Factory(self.factoryname,self.fout,self.factoryoption)
        self.dataloader=ROOT.TMVA.DataLoader(self.factoryname)
        ##--variables
        for this_var in self.variables:
            self.dataloader.AddVariable(this_var)
        for this_s in self.spectators:
            self.dataloader.AddSpectator(this_s)

        self.dataloader.AddSignalTree(self.dict_tree["sig_test"],1.0,"test") ## "train_test could be train or test"
        self.dataloader.AddSignalTree(self.dict_tree["sig_train"],1.0,"train") ## "train_test could be train or test"

        self.dataloader.AddBackgroundTree(self.dict_tree["bkg_test"],1.0,"test") ## "train_test could be train or test"
        self.dataloader.AddBackgroundTree(self.dict_tree["bkg_train"],1.0,"train") ## "train_test could be train or test"

        self.dataloader.SetSignalWeightExpression(self.weight_exp_sig)
        self.dataloader.SetBackgroundWeightExpression(self.weight_exp_bkg)
        print(">>>>self.dataloader.PrepareTrainingAndTestTree")
        print("Set sig cut ->",self.cut_sig)
        print("Set bkg cut ->",self.cut_bkg)
        self.dataloader.PrepareTrainingAndTestTree(ROOT.TCut(self.cut_sig),ROOT.TCut(self.cut_bkg),self.dataoption)
        for method in self.methodlist:
            method['options']=method['options'].replace("__NTrees__",str(self.NTrees))
            method['options']=method['options'].replace("__MinNodeSize__",str(self.MinNodeSize))
            method['options']=method['options'].replace("__MaxDepth__",str(self.MaxDepth))
            method['options']=method['options'].replace("__BoostType__",str(self.BoostType))
            method['options']=method['options'].replace("__AdaBoostBeta__",str(self.AdaBoostBeta))
            method['options']=method['options'].replace("__UseBaggedBoost__",str(self.UseBaggedBoost))
            method['options']=method['options'].replace("__BaggedSampleFraction__",str(self.BaggedSampleFraction))
            method['options']=method['options'].replace("__SeparationType__",str(self.SeparationType))
            method['options']=method['options'].replace("__nCuts__",str(self.nCuts))
            method['options']=method['options'].replace("__IgnoreNegWeightsInTraining__",str(self.IgnoreNegWeightsInTraining))            
            
            self.factory.BookMethod(self.dataloader,
                               method['type'],
                               method['name'],
                               method['options']
            )
        
        
    def SetTreeInfo(self):
        print("---sig_test---")
        print("<self.testtree_sig>",self.testtree_sig)
        self.dict_tree["sig_test"]=ROOT.TChain(self.testtree_sig)
        for _path in self.testinputlist_sig:
            print(_path)
            self.dict_tree["sig_test"].Add(_path)
        print("--bkg_test---")
        print("<self.testtree_bkg>",self.testtree_bkg)
        self.dict_tree["bkg_test"]=ROOT.TChain(self.testtree_bkg)
        for _path in self.testinputlist_bkg:
            print(_path)
            self.dict_tree["bkg_test"].Add(_path)
        print("---sig_train---")
        print("<self.traintree_sig>",self.traintree_sig)
        self.dict_tree["sig_train"]=ROOT.TChain(self.traintree_sig)
        for _path in self.traininputlist_sig:
            print(_path)
            self.dict_tree["sig_train"].Add(_path)
        print("---bkg_train---")
        print("<self.traintree_bkg>",self.traintree_bkg)
        self.dict_tree["bkg_train"]=ROOT.TChain(self.traintree_bkg)
        for _path in self.traininputlist_bkg:
            print(_path)
            self.dict_tree["bkg_train"].Add(_path)


    def InitTMVA(self):
        ROOT.TMVA.gConfig().GetVariablePlotting().fNbinsMVAoutput = 100
        ROOT.gROOT.SetBatch()
        ROOT.TMVA.Tools.Instance()##intialize
        


    def __del__(self):
        pass
        #del self.dict_tree
        #del self.dataloader
        #del self.factory
        #del self.fout

if __name__ == '__main__':
    name="mytest"
    test=TMVA_TOOL()
    test.SetFactoryName(name)
    test.SetInputVariables(["bjet_pt","bjet_aeta"])
    test.SetSpectators(["bjet_partonFlavour","lhe_b_pdgid","bjet_partonFlavour*lhe_b_pdgid>0"])
    test.SetCut_Sig("(bmuon_charge*bjet_partonFlavour < 0)*Has_bMuon")
    test.SetCut_Bkg("(bmuon_charge*bjet_partonFlavour > 0)*Has_bMuon")

    test.SetTransform("G")
    test.SetTestTreeAndInput_Sig("OutTree/sig",["../inputs/EEMu_MuMuE_Method/v2409.2/2017/EEMu_MuMuE_Method_DYJetsToEE_MiNNLO.root","../inputs/EEMu_MuMuE_Method/v2409.2/2017/EEMu_MuMuE_Method_DYJetsToMuMu_MiNNLO.root"])
    test.SetTrainTreeAndInput_Sig("OutTree/sig",["../inputs/EEMu_MuMuE_Method/v2409.2/2017/EEMu_MuMuE_Method_DYJets.root"])
    test.SetTestTreeAndInput_Bkg("OutTree/bkg",["../inputs/EEMu_MuMuE_Method/v2409.2/2017/EEMu_MuMuE_Method_DYJetsToEE_MiNNLO.root","../inputs/EEMu_MuMuE_Method/v2409.2/2017/EEMu_MuMuE_Method_DYJetsToMuMu_MiNNLO.root"])
    test.SetTrainTreeAndInput_Bkg("OutTree/bkg",["../inputs/EEMu_MuMuE_Method/v2409.2/2017/EEMu_MuMuE_Method_DYJets.root"])
    test.SetWeight_Sig("1.")
    test.SetWeight_Bkg("1.")
    test.SetOutputName(name+".root")
    test.Run()
