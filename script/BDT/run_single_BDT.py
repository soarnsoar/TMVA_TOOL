#!/usr/bin/env python3
##-----
import os
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
import sys
def GetVariableConfig(version):
        version=str(version)
        sys.path.append(maindir+"/config/ForBDT/v"+version)
        import variables as _variables
        #exec(open(maindir+"/config/v"+version+"/variables.py"))
        print(_variables.bmuon_var,_variables.belectron_var,_variables.bjet_var)
        return _variables.bmuon_var,_variables.belectron_var,_variables.bjet_var
def GetCutConfig(version):
        version=str(version)
        #exec(open(maindir+"/config/v"+version+"/cuts.py"))
        sys.path.append(maindir+"/config/ForBDT/v"+version)
        import cuts as _cuts
        print(_cuts.bmuon_sigcut, _cuts.bmuon_bkgcut, _cuts.belectron_sigcut, _cuts.belectron_bkgcut, _cuts.bjet_sigcut, _cuts.bjet_bkgcut)
        return _cuts.bmuon_sigcut, _cuts.bmuon_bkgcut, _cuts.belectron_sigcut, _cuts.belectron_bkgcut, _cuts.bjet_sigcut, _cuts.bjet_bkgcut
if __name__== '__main__':
        import argparse
        parser = argparse.ArgumentParser(description='input argument')
        
        parser.add_argument('--name', dest='name', default="", help="name")
        parser.add_argument('--version', dest='version', default="", help="version")
        parser.add_argument('--year', dest='year', default="", help="year")        
        parser.add_argument('--channel', dest='channel', default="", help="muon/electron/jet")    


        parser.add_argument('--analyzer', dest='analyzer', default="", help="analyzer")        

        parser.add_argument('--transform', dest='transform', default="", help="transform")        

        parser.add_argument('--VarToSkip', dest='VarToSkip', default="", help="Don't use this variable for the training")


        #####BDT Vars ####
        parser.add_argument('--NTrees', dest='NTrees', default="", help="NTrees")
        parser.add_argument('--MaxDepth', dest='MaxDepth', default="", help="MaxDepth")
        parser.add_argument('--Shrinkage', dest='Shrinkage', default="", help="Shrinkage(Only For GradBoost algo)")
        parser.add_argument('--MinNodeSize', dest='MinNodeSize', default="", help="MinNodeSize")
        parser.add_argument('--BoostType', dest='BoostType', default="", help="BoostType")
        parser.add_argument('--AdaBoostBeta', dest='AdaBoostBeta', default="", help="AdaBoostBeta(Only For AdaBoost BoostType)")
        parser.add_argument('--UseBaggedBoost', dest='UseBaggedBoost', default="", help="UseBaggedBoost(Random Sampling for avoiding overfit")
        parser.add_argument('--BaggedSampleFraction', dest='BaggedSampleFraction', default="", help="BaggedSampleFraction(Only For UseBaggedBoost)")
        parser.add_argument('--SeparationType', dest='SeparationType', default="", help="SeparationType")
        parser.add_argument('--nCuts', dest='nCuts', default="", help="nCuts")
        parser.add_argument('--IgnoreNegWeightsInTraining', dest='IgnoreNegWeightsInTraining', default="", help="IgnoreNegWeightsInTraining")

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



        from TMVA_BDT_single import TMVA_TOOL
        test=TMVA_TOOL()
        test.SetFactoryName(name)
        test.SetInputVariables(variables)
        test.SetSpectators(["bjet_partonFlavour","lhe_b_pdgid","bjet_partonFlavour*lhe_b_pdgid>0","bmuon_charge","belectron_charge","bjet_charge"])
        print('sigcut=',sigcut)
        print('bkgcut=',bkgcut)
        test.SetCut_Sig(sigcut)
        test.SetCut_Bkg(bkgcut)
        
        ##---BDT Params---##
        test.SetNTrees(args.NTrees)
        test.SetMaxDepth(args.MaxDepth)
        test.SetShrinkage(args.Shrinkage)
        test.SetMinNodeSize(args.MinNodeSize)
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
