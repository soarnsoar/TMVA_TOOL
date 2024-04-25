from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Add, Lambda
#from keras.layers.noise import GaussianNoise
from keras.layers.normalization import BatchNormalization
from keras import initializers
from keras import regularizers
from keras.optimizers import SGD, Adam, Nadam

import ROOT
import os

class TMVA_DNN_TOOL:
    def __init__(self):
        self.dict_tree={}
        self.methodlist=[]
        ##--Set Default setup
        self.SetActivationOut("softmax")
        self.SetActivationHidden("selu")
        self.SetFactoryName("TMVAClassification")
        self.SetOutModelName("model.h5")
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
            'type' : ROOT.TMVA.Types.kPyKeras,
            'name' : "DNN",
            'options' : ":".join(["H",
                                  "!V",
                                  #"VarTransform=N,D",
                                  "VarTransform=G",
                                  "FilenameModel=__outmodelname__",
                                  "NumEpochs=__nepoch__",
                                  "SaveBestOnly=false",
                                  "BatchSize=__batchsize__",
                                  "verbose=2",
                                  "TriesEarlyStopping=30",
                                  #"IgnoreNegWeightsInTraining=True",
                              ])
        }
                       )
        self.SetNnode(128)
        self.SetDropout(0.2)
        self.SetLossFunction("categorical_crossentropy")
        self.SetOptimizer(Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004))
        self.SetMetrics(['accuracy'])
        self.SetDataOption("!V")
    def SetInputVariables(self,_variables):
        self.variables=_variables
        self.input_dim=len(self.variables)
    def SetSpectators(self,_spectators):
        self.spectators=_spectators
    def SetCut_Sig(self,cut_exp):
        self.cut_sig=cut_exp
    def SetCut_Bkg(self,cut_exp):
        self.cut_bkg=cut_exp
    def SetNlayer(self,nlayer):
        self.nlayer=nlayer
    def SetActivationHidden(self,actname):
        self.activation_hidden=actname
    def SetActivationOut(self,actname):
        self.activation_output=actname
    def SetDropout(self,dropout):
        self.dropout=dropout
    def SetNnode(self,nnode):
        self.nNode=nnode
    def SetLossFunction(self,lossftn):
        self.lossftn=lossftn
    def SetOptimizer(self,_optimizer):
        self.optimizer=_optimizer
    def SetMetrics(self,_metrics):
        self.metrics=_metrics
    def SetOutModelName(self,outmodelname):
        self.outmodelname=outmodelname
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
    def SetNepoch(self,nepoch):
        self.nepoch=nepoch
    def SetBatchSize(self,batchsize):
        self.batchsize=batchsize
    def AddMethod(self,_method):
        self.methodlist.append(_method)
    def SetOutputName(self,outputname):
        self.outputname=outputname
    def Run(self):
        self.GenerateKerasModel()
        self.InitTMVA()
        self.SetTreeInfo()
        self.SetFactory()
        self.RunTrain()
    def RunTrain(self):
        self.factory.TrainAllMethods()
        self.factory.TestAllMethods()
        self.factory.EvaluateAllMethods()
        for method in self.methodlist:
            _cut=self.factory.GetMethod(self.factoryname,method['name']).GetSignalReferenceCut()
            print "ref.cut=",method['name'],_cut
            #_sigeff=self.factory.GetMethod(self.factoryname,method['name']).GetEfficiency(_cut,"SigEff")
            #print "sig.eff=",_sigeff
            #_bkgeff=self.factory.GetMethod(self.factoryname,method['name']).GetEfficiency(_cut,"BkgEff")
            #print "bkg.eff=",_sigeff
        self.fout.Close()
        
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
        self.dataloader.PrepareTrainingAndTestTree(ROOT.TCut(self.cut_sig),ROOT.TCut(self.cut_bkg),self.dataoption)
        for method in self.methodlist:
            method['options']=method['options'].replace("__nepoch__",str(self.nepoch))
            method['options']=method['options'].replace("__batchsize__",str(self.batchsize))
            method['options']=method['options'].replace("__outmodelname__",str(self.outmodelname))
            self.factory.BookMethod(self.dataloader,
                               method['type'],
                               method['name'],
                               method['options']
            )
        
        
    def SetTreeInfo(self):
        self.dict_tree["sig_test"]=ROOT.TChain(self.testtree_sig)
        for _path in self.testinputlist_sig:
            self.dict_tree["sig_test"].Add(_path)

        self.dict_tree["bkg_test"]=ROOT.TChain(self.testtree_bkg)
        for _path in self.testinputlist_bkg:
            self.dict_tree["bkg_test"].Add(_path)

        self.dict_tree["sig_train"]=ROOT.TChain(self.traintree_sig)
        for _path in self.traininputlist_sig:
            self.dict_tree["sig_train"].Add(_path)

        self.dict_tree["bkg_train"]=ROOT.TChain(self.traintree_bkg)
        for _path in self.traininputlist_bkg:
            self.dict_tree["bkg_train"].Add(_path)


    def InitTMVA(self):
        ROOT.TMVA.gConfig().GetVariablePlotting().fNbinsMVAoutput = 100
        ROOT.gROOT.SetBatch()
        ROOT.TMVA.Tools.Instance()##intialize
        ROOT.TMVA.PyMethodBase.PyInitialize()  ## init for c++ <-> python

    def GenerateKerasModel(self):
        self.mykeras=Sequential()
        self.mykeras.add(Dense(self.nNode,
                input_shape=(self.input_dim,),
                kernel_initializer=initializers.he_normal(seed=1231),
                kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-5)))
        self.mykeras.add(BatchNormalization())
        self.mykeras.add(Activation(self.activation_hidden))
        self.mykeras.add(Dropout(self.dropout))
        
        for i in range(self.nlayer-1):
            self.mykeras.add(Dense(self.nNode, kernel_initializer=initializers.he_normal(seed=1231), kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-5)))
            self.mykeras.add(BatchNormalization())
            self.mykeras.add(Activation(self.activation_hidden))
            self.mykeras.add(Dropout(self.dropout))
        self.mykeras.add(Dense(2, kernel_initializer=initializers.RandomUniform(minval=-0.05, maxval=0.05, seed=1234)))
        self.mykeras.add(Activation(self.activation_output))
        self.mykeras.compile(loss=self.lossftn,optimizer=self.optimizer,metrics=self.metrics)
        self.mykeras.save(self.outmodelname)
        self.mykeras.summary()

if __name__ == '__main__':
    name="mytest"
    test=TMVA_DNN_TOOL()
    test.SetFactoryName(name)
    test.SetInputVariables(["bjet_pt","bjet_aeta"])
    test.SetSpectators(["bjet_partonFlavour","lhe_b_pdgid","bjet_partonFlavour*lhe_b_pdgid>0"])
    test.SetCut_Sig("(bmuon_charge*bjet_partonFlavour < 0)*Has_bMuon")
    test.SetCut_Bkg("(bmuon_charge*bjet_partonFlavour > 0)*Has_bMuon")
    test.SetNlayer(5)
    test.SetDropout(0.2)
    test.SetTestTreeAndInput_Sig("OutTree/sig",["../inputs/bChargeID_TrainTree/2017/bChargeID_TrainTree_SkimTree_Dilepton_DYJets_MG.root"])
    test.SetTrainTreeAndInput_Sig("OutTree/sig",["../inputs/bChargeID_TrainTree/2017/bChargeID_TrainTree_SkimTree_Dilepton_DYJets.root"])
    test.SetTestTreeAndInput_Bkg("OutTree/bkg",["../inputs/bChargeID_TrainTree/2017/bChargeID_TrainTree_SkimTree_Dilepton_DYJets_MG.root"])
    test.SetTrainTreeAndInput_Bkg("OutTree/bkg",["../inputs/bChargeID_TrainTree/2017/bChargeID_TrainTree_SkimTree_Dilepton_DYJets.root"])
    test.SetWeight_Sig("1.")
    test.SetWeight_Bkg("1.")
    test.SetNepoch(100)
    test.SetBatchSize(1000)
    test.SetOutputName(name+".root")
    test.Run()
