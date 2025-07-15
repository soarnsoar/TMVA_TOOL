#!/usr/bin/env python
##-----
import ROOT
import os
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
def GetVariableConfig(version):
        version=str(version)
	exec(open(maindir+"/config/TTSemiLepJetAssignment_ProduceTrainingTree/v"+version+"/variables.py"))
        return input_variables
def GetCutConfig(version):
        version=str(version)
	exec(open(maindir+"/config/TTSemiLepJetAssignment_ProduceTrainingTree/v"+version+"/cuts.py"))
        return sigcut,bkgcut
if __name__== '__main__':
        import argparse
        parser = argparse.ArgumentParser(description='input argument')
        parser.add_argument('--nlayer', dest='nlayer', default="5", help="nlayyer")
        parser.add_argument('--name', dest='name', default="dnn", help="name")

        parser.add_argument('--nnode', dest='nnode', default="", help="nnode")
        parser.add_argument('--nepoch', dest='nepoch', default="", help="nepoch")
        parser.add_argument('--batchsize', dest='batchsize', default="", help="batchsize")
        parser.add_argument('--dropout', dest='dropout', default="", help="dropout")
        parser.add_argument('--version', dest='version', default="", help="version")    

        parser.add_argument('--year', dest='year', default="", help="year")        
        parser.add_argument('--analyzer', dest='analyzer', default="", help="year")        

        parser.add_argument('--transform', dest='transform', default="I", help="transform")        
        parser.add_argument('--flag', dest='flag', default="", help="useflag in skflat")        

        args = parser.parse_args()
        
        nlayer=int(args.nlayer)
        nnode=int(args.nnode)
        nepoch=int(args.nepoch)
        batchsize=int(args.batchsize)
        dropout=float(args.dropout)
        name=args.name
        version=args.version

        analyzer=args.analyzer
        year=args.year

        transform=args.transform
        flag=args.flag


        variables=GetVariableConfig(version)
        sigcut,bkgcut=GetCutConfig(version)


        from TMVA_DNN import TMVA_DNN_TOOL

        test=TMVA_DNN_TOOL()
        test.SetFactoryName(name)
        test.SetInputVariables(variables)
        test.SetSpectators([])
        test.SetCut_Sig(sigcut)
        test.SetCut_Bkg(bkgcut)
        test.SetNlayer(nlayer)
        test.SetNnode(nnode)
        test.SetDropout(dropout)
        #test.SetDataOption("!V:nTrain_Signal=1000000:nTrain_Background=1000000:SplitMode=Random")
        test.SetDataOption("!V:SplitMode=Random")

        #TTSemiLepJetAssignment_ProduceTrainingTree_TTLJ_powheg.root
        test.SetTestTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+analyzer+"/"+year+"/"+flag+"/"+analyzer+"_TTLJ_powheg.root"])
        test.SetTrainTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+analyzer+"/"+year+"/"+flag+"/"+analyzer+"_TTLJ_powheg.root"])

        test.SetTestTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/"+year+"/"+flag+"/"+analyzer+"_TTLJ_powheg.root"])
        test.SetTrainTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/"+year+"/"+flag+"/"+analyzer+"_TTLJ_powheg.root"])

        test.SetWeight_Sig("weight")
        test.SetWeight_Bkg("weight")
        test.SetNepoch(nepoch)
        test.SetBatchSize(batchsize)
        test.SetTransform(transform)
        test.SetOutputName(name+".root")
        test.Run()
