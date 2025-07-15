#!/usr/bin/env python3
##-----
import os
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
import sys
def GetVariableConfig(version):
        version=str(version)
        sys.path.append(maindir+"/config/v"+version)
        print(maindir+"/config/v"+version)
        import variables as _variables
        #exec(open(maindir+"/config/v"+version+"/variables.py"))
        return _variables.bmuon_var,_variables.belectron_var,_variables.bjet_var
def GetCutConfig(version):
        version=str(version)
        #exec(open(maindir+"/config/v"+version+"/cuts.py"))
        sys.path.append(maindir+"/config/v"+version)
        import cuts as _cuts
        return _cuts.bmuon_sigcut, _cuts.bmuon_bkgcut, _cuts.belectron_sigcut, _cuts.belectron_bkgcut, _cuts.bjet_sigcut, _cuts.bjet_bkgcut
if __name__== '__main__':
        import argparse
        parser = argparse.ArgumentParser(description='input argument')
        
        parser.add_argument('--name', dest='name', default="BDT", help="name")
        parser.add_argument('--version', dest='version', default="2409.2", help="version")    
        parser.add_argument('--channel', dest='channel', default="muon", help="muon/electron/jet")    

        parser.add_argument('--year', dest='year', default="2017", help="year")        
        parser.add_argument('--analyzer', dest='analyzer', default="EEMu_MuMuE_Method", help="analyzer")        

        parser.add_argument('--transform', dest='transform', default="G", help="transform")        

        parser.add_argument('--VarToSkip', dest='VarToSkip', default="", help="Don't use this variable for the training")


        #####BDT Vars ####
        parser.add_argument('--NTrees', dest='NTrees', default="800", help="NTrees")
        parser.add_argument('--MaxDepth', dest='MaxDepth', default="3", help="MaxDepth")
        parser.add_argument('--Shrinkage', dest='Shrinkage', default="1", help="Shrinkage(Only For GradBoost algo)")
        parser.add_argument('--MinNodeSize', dest='MinNodeSize', default="5", help="MinNodeSize")
        parser.add_argument('--BoostType', dest='BoostType', default="AdaBoost", help="BoostType")
        parser.add_argument('--AdaBoostBeta', dest='AdaBoostBeta', default="0.5", help="AdaBoostBeta(Only For AdaBoost BoostType)")
        parser.add_argument('--UseBaggedBoost', dest='UseBaggedBoost', default="False", help="UseBaggedBoost")
        parser.add_argument('--BaggedSampleFraction', dest='BaggedSampleFraction', default="0.6", help="BaggedSampleFraction(Only For UseBaggedBoost)")
        parser.add_argument('--SeparationType', dest='SeparationType', default="GiniIndex", help="SeparationType")
        parser.add_argument('--nCuts', dest='nCuts', default="20", help="nCuts")
        parser.add_argument('--IgnoreNegWeightsInTraining', dest='IgnoreNegWeightsInTraining', default="False", help="IgnoreNegWeightsInTraining")

        #################

        args = parser.parse_args()
        

        name=args.name
        version=args.version
        channel=args.channel


        analyzer=args.analyzer
        year=args.year

        transform=args.transform




        VarToSkip=args.VarToSkip.split()


        bmuon_var,belectron_var,bjet_var=GetVariableConfig(version)
        bmuon_sigcut,bmuon_bkgcut,belectron_sigcut,belectron_bkgcut,bjet_sigcut,bjet_bkgcut=GetCutConfig(version)
        variables=[]


        sigcut=""
        bkgcut=""
        if channel=="muon":
                if VarToSkip:
                        if VarToSkip in bmuon_var : 
                                for v in VarToSkip :
                                        bmuon_var.remove(v)
                        if VarToSkip in bjet_var  :
                                for v in VarToSkip:
                                        bjet_var.remove(v)
                variables=bmuon_var+bjet_var
                sigcut=bmuon_sigcut
                bkgcut=bmuon_bkgcut
                
        elif channel=="electron":
                if VarToSkip:
                        if VarToSkip in belectron_var : 
                                for v in VarToSkip :
                                        belectron_var.remove(v)
                        if VarToSkip in bjet_var  :
                                for v in VarToSkip:
                                        bjet_var.remove(v)
                variables=belectron_var+bjet_var
                sigcut=belectron_sigcut
                bkgcut=belectron_bkgcut
        elif channel=="jet":
                if VarToSkip in bjet_var  :
                        for v in VarToSkip:
                                bjet_var.remove(v)

                variables=bjet_var+[]
                sigcut=bjet_sigcut
                bkgcut=bjet_bkgcut
        else:
                print("[run_nnode_nlayer_nepoch_batchsize.py]Wrong channel input")
                channel
                1/0



        from TMVA_BDT import TMVA_TOOL
        test=TMVA_TOOL()
        test.SetFactoryName(name)
        test.SetInputVariables(variables)
        test.SetSpectators(["bjet_partonFlavour","lhe_b_pdgid","bjet_partonFlavour*lhe_b_pdgid>0","bmuon_charge","belectron_charge","bjet_charge"])
        
        test.SetCut_Sig(sigcut)
        test.SetCut_Bkg(bkgcut)
        
        ##---BDT Params---##
        test.SetNTrees(args.NTrees)
        test.SetMinNodeSize(args.MinNodeSize)
        test.SetMaxDepth(args.MaxDepth)
        test.SetBoostType(args.BoostType)
        test.SetAdaBoostBeta(args.AdaBoostBeta)
        test.SetUseBaggedBoost(args.UseBaggedBoost)
        test.SetBaggedSampleFraction(args.BaggedSampleFraction)
        test.SetSeparationType(args.SeparationType)
        test.SetnCuts(args.nCuts)
        test.SetIgnoreNegWeightsInTraining(args.IgnoreNegWeightsInTraining)


        test.SetTestTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToMuMu_MiNNLO.root"])

        test.SetTrainTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets.root"])
        test.SetTestTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToMuMu_MiNNLO.root"])

        test.SetTrainTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets.root"])
        test.SetWeight_Sig("weight")
        test.SetWeight_Bkg("weight")
        
        
        test.SetTransform(transform)
        test.SetOutputName(name+".root")
        test.Run()
        print("END of RUNNING...run_single")
