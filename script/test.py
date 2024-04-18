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
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
testinput=maindir+"/inputs/test/ForLepJetChargeReliability_DYJets.root"

variables={
    "belectron_eta":{
        "definition":"belectron_eta",
        "type":"D"
    },
    "belectron_pt":{
        "definition":"belectron_pt",
        "type":"D"
    },
}
sig_cut_exp="1."
bkg_cut_exp="1."

activation_hidden='selu'
activation_output='softmax'
input_dim= len(variables) ##number of input variables
#nlayer=5
dropout=0.5
nNode=128
lossftn="categorical_crossentropy"
optimizer_=Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)
metrics_=['accuracy',]
outputname="model.h5"

factoryname="TMVAClassification"
factoryoption=":".join(["!V",
                        "!Silent",
                        "Color",
                        "DrawProgressBar",
                        "Transformations=I",
                        "AnalysisType=Classification",
                    ])

sig_test_treename="OutTree/Tree_LepChargeMatch_Group1"
sig_test_rootfile_list=[testinput]

sig_train_treename="OutTree/Tree_LepChargeMatch_Group2"
sig_train_rootfile_list=[testinput]

bkg_test_treename="OutTree/Tree_LepChargeUnmatch_Group1"
bkg_test_rootfile_list=[testinput]

bkg_train_treename="OutTree/Tree_LepChargeUnmatch_Group2"
bkg_train_rootfile_list=[testinput]

weight_exp="weight"
data_options="!V"
## SplitMode=Alternate sig->bkg->sig->bkg...
## SplitMode=Random -> random

nepoch=10 ## number of iterations
batchsize=1000 ## every this number of events, weights are updated
methodlist=[
    {
        'type' : ROOT.TMVA.Types.kPyKeras,
        'name' : "DNN",
        'options' : ":".join(["H",
                              "!V",
                              #"VarTransform=N,D",
                              "VarTransform=G",
                              "FilenameModel=model.h5",
                              "NumEpochs="+str(nepoch),
                              "SaveBestOnly=false",
                              "BatchSize="+str(batchsize),
                              "verbose=2",
                              "TriesEarlyStopping=30",
                              #"IgnoreNegWeightsInTraining=True",
                          ])
    },
]    

outFileName="test_output.root"
###-----End of Option
mymodel = Sequential()


##---1st layer
mymodel.add(Dense(nNode, 
                input_shape=(input_dim,),  
                kernel_initializer=initializers.he_normal(seed=1231), 
                kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-5)))
##kernal_initializer => set random seed, he_normal -> going well with Relu 
##regularizerm l1 -> penalty proportional to abs(weight) // l2 -> penalty proportion to w**2
mymodel.add(BatchNormalization())
mymodel.add(Activation(activation_hidden))
mymodel.add(Dropout(dropout))

##----output layer 
mymodel.add(Dense(2, kernel_initializer=initializers.RandomUniform(minval=-0.05, maxval=0.05, seed=1234)))
##number of node==2, which means two kinds of values will be output.(e.g) prob. of sig and prob. of bkg??
##make weight random value [minval, maxval]
mymodel.add(Activation(activation_output))
##softmax function of x1 = exp(x1)/{exp(x1)+exp(x2)+exp(x3)+...}
##--all output = [0,1]
## sum of output=1
##(e.g) prob. of sig + prob. of bkg = 1

mymodel.compile(loss=lossftn, optimizer=optimizer_, metrics=metrics_)
mymodel.save(outputname)
mymodel.summary()

###---Now, we have compiled keras model file, "model.h5"
### put this model to TMVA

ROOT.TMVA.gConfig().GetVariablePlotting().fNbinsMVAoutput = 100
ROOT.gROOT.SetBatch()
ROOT.TMVA.Tools.Instance()##intialize
ROOT.TMVA.PyMethodBase.PyInitialize()  ## init for c++ <-> python

spectators={}
cuts={}

dict_tree={}
##---input treefiles

dict_tree["sig_test"]=ROOT.TChain(sig_test_treename)
for _path in sig_test_rootfile_list:
    dict_tree["sig_test"].Add(_path)

dict_tree["sig_train"]=ROOT.TChain(sig_train_treename)
for _path in sig_train_rootfile_list:
    dict_tree["sig_train"].Add(_path)

dict_tree["bkg_test"]=ROOT.TChain(bkg_test_treename)
for _path in bkg_test_rootfile_list:
    dict_tree["bkg_test"].Add(_path)

dict_tree["bkg_train"]=ROOT.TChain(bkg_train_treename)
for _path in bkg_train_rootfile_list:
    dict_tree["bkg_train"].Add(_path)





fout = ROOT.TFile(outFileName,"RECREATE")
factory=ROOT.TMVA.Factory(factoryname,fout,factoryoption)
dataloader=ROOT.TMVA.DataLoader(factoryname)
for this_var in variables:
    _definition=variables[this_var]["definition"]
    _type=variables[this_var]["type"]
    dataloader.AddVariable(_definition,_type)
dataloader.AddSignalTree(dict_tree["sig_test"],1.0,"test") ## "train_test could be train or test"
dataloader.AddSignalTree(dict_tree["sig_train"],1.0,"train") ## "train_test could be train or test"
## arg1 = tree , arg2 = weight, arg3 = tree type 
dataloader.AddBackgroundTree(dict_tree["bkg_test"],1.0,"train_test") ## "train_test could be train or test"
dataloader.AddBackgroundTree(dict_tree["bkg_train"],1.0,"train_train") ## "train_test could be train or test"
dataloader.SetSignalWeightExpression(weight_exp)
dataloader.SetBackgroundWeightExpression(weight_exp)
dataloader.PrepareTrainingAndTestTree(ROOT.TCut(sig_cut_exp),ROOT.TCut(bkg_cut_exp),data_options)

##book method
for method in methodlist:
    factory.BookMethod(dataloader,
                             method['type'],
                       method['name'],
                       method['options']
                   )
##--train
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
##--get reference cut
for method in methodlist:
    cut=factory.GetMethod(factoryname,method['name']).GetSignalReferenceCut()
    print method['name'],cut
fout.Close()
