#!/usr/bin/env python
##-----
import os
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
def GetVariableConfig(version):
        version=str(version)
	exec(open(maindir+"/config/v"+version+"/variables.py"))
        return bmuon_var,belectron_var,bjet_var
if __name__== '__main__':
        import argparse
        parser = argparse.ArgumentParser(description='input argument')
        parser.add_argument('--nlayer', dest='nlayer', default="5", help="nlayyer")
        parser.add_argument('--name', dest='name', default="dnn", help="name")
        parser.add_argument('--nnode', dest='nnode', default="128", help="nnode")
        parser.add_argument('--nepoch', dest='nepoch', default="300", help="nepoch")
        parser.add_argument('--batchsize', dest='batchsize', default="1000", help="batchsize")
        parser.add_argument('--dropout', dest='dropout', default="0.2", help="dropout")
        parser.add_argument('--version', dest='version', default="1.0", help="version")    
        parser.add_argument('--channel', dest='channel', default="-", help="muon/electron/jet")    
        
        args = parser.parse_args()
        
        nlayer=int(args.nlayer)
        nnode=int(args.nnode)
        nepoch=int(args.nepoch)
        batchsize=int(args.batchsize)
        dropout=float(args.dropout)
        name=args.name
        version=args.version
        channel=args.channel

        bmuon_var,belectron_var,bjet_var=GetVariableConfig(version)
        variables=[]


        sigcut=""
        bkgcut=""
        if channel=="muon":
                variables=bmuon_var+bjet_var
                sigcut="(bmuon_charge*bjet_partonFlavour < 0)*Has_bMuon"
                bkgcut="(bmuon_charge*bjet_partonFlavour > 0)*Has_bMuon"
        elif channel=="electron":
                variables=belectron_var+bjet_var
                sigcut="(belectron_charge*bjet_partonFlavour < 0)*(Has_bElectron)*(!Has_bMuon)"
                bkgcut="(belectron_charge*bjet_partonFlavour > 0)*(Has_bElectron)*(!Has_bMuon)"
        elif channel=="jet":
                variables=bjet_var
                sigcut="(bjet_charge*bjet_partonFlavour < 0)*(!Has_bElectron)*(!Has_bMuon)"
                bkgcut="(bjet_charge*bjet_partonFlavour > 0)*(!Has_bElectron)*(!Has_bMuon)"
        else:
                print "[run_nnode_nlayer_nepoch_batchsize.py]Wrong channel input"
                channel
                1/0



        from TMVA_DNN import TMVA_DNN_TOOL
        test=TMVA_DNN_TOOL()
        test.SetFactoryName(name)
        test.SetInputVariables(variables)
        test.SetSpectators(["bjet_partonFlavour","lhe_b_pdgid","bjet_partonFlavour*lhe_b_pdgid>0"])
        test.SetCut_Sig("(bmuon_charge*bjet_partonFlavour < 0)*Has_bMuon")
        test.SetCut_Bkg("(bmuon_charge*bjet_partonFlavour > 0)*Has_bMuon")
        test.SetNlayer(nlayer)
        test.SetDropout(dropout)
        test.SetTestTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/bChargeID_TrainTree/2017/bChargeID_TrainTree_SkimTree_Dilepton_DYJets_MG.root"])
        test.SetTrainTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/bChargeID_TrainTree/2017/bChargeID_TrainTree_SkimTree_Dilepton_DYJets.root"])
        test.SetTestTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/bChargeID_TrainTree/2017/bChargeID_TrainTree_SkimTree_Dilepton_DYJets_MG.root"])
        test.SetTrainTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/bChargeID_TrainTree/2017/bChargeID_TrainTree_SkimTree_Dilepton_DYJets.root"])
        test.SetWeight_Sig("weight")
        test.SetWeight_Bkg("weight")
        test.SetNepoch(nepoch)
        test.SetBatchSize(batchsize)
        test.SetOutputName(name+".root")
        test.Run()
