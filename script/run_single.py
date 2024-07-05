#!/usr/bin/env python
##-----
import os
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
def GetVariableConfig(version):
        version=str(version)
	exec(open(maindir+"/config/v"+version+"/variables.py"))
        return bmuon_var,belectron_var,bjet_var
def GetCutConfig(version):
        version=str(version)
	exec(open(maindir+"/config/v"+version+"/cuts.py"))
        return bmuon_sigcut,bmuon_bkgcut,belectron_sigcut,belectron_bkgcut,bjet_sigcut,bjet_bkgcut
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
        parser.add_argument('--channel', dest='channel', default="-", help="muon/electron/jet")    
        parser.add_argument('--switch', dest='switch', action="store_true",default=False, help="switch sig/bkg")    
        parser.add_argument('--useLO', dest='useLO', action="store_true",default=False, help="useLO")    

        parser.add_argument('--year', dest='year', default="", help="year")        
        parser.add_argument('--analyzer', dest='analyzer', default="", help="year")        

        parser.add_argument('--transform', dest='transform', default="I", help="transform")        

        parser.add_argument('--VarToSkip', dest='VarToSkip', default="", help="Don't use this variable for the training")


        args = parser.parse_args()
        
        nlayer=int(args.nlayer)
        nnode=int(args.nnode)
        nepoch=int(args.nepoch)
        batchsize=int(args.batchsize)
        dropout=float(args.dropout)
        name=args.name
        version=args.version
        channel=args.channel
        switch=args.switch

        analyzer=args.analyzer
        year=args.year

        transform=args.transform
        useLO=args.useLO

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
                print "[run_nnode_nlayer_nepoch_batchsize.py]Wrong channel input"
                channel
                1/0



        from TMVA_DNN import TMVA_DNN_TOOL
        test=TMVA_DNN_TOOL()
        test.SetFactoryName(name)
        test.SetInputVariables(variables)
        test.SetSpectators(["bjet_partonFlavour","lhe_b_pdgid","bjet_partonFlavour*lhe_b_pdgid>0","bmuon_charge","belectron_charge","bjet_charge"])
        if switch:
                print "!!!switch sig <-> bkg input events!!!"
                test.SetCut_Sig(bkgcut)
                test.SetCut_Bkg(sigcut)
        else:
                test.SetCut_Sig(sigcut)
                test.SetCut_Bkg(bkgcut)
        test.SetNlayer(nlayer)
        test.SetNnode(nnode)
        test.SetDropout(dropout)



        if switch:
                test.SetTestTreeAndInput_Bkg("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToMuMu_MiNNLO.root"])
                if useLO:
                        test.SetTrainTreeAndInput_Bkg("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets_MG.root"])
                else:
                        test.SetTrainTreeAndInput_Bkg("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets.root"])
                test.SetTestTreeAndInput_Sig("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToMuMu_MiNNLO.root"])
                if useLO:
                        test.SetTrainTreeAndInput_Sig("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets_MG.root"])
                else:
                        test.SetTrainTreeAndInput_Sig("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets.root"])
        else:
                test.SetTestTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToMuMu_MiNNLO.root"])
                if useLO:
                        test.SetTrainTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets_MG.root"])
                else:
                        test.SetTrainTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets.root"])
                test.SetTestTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToMuMu_MiNNLO.root"])
                if useLO:
                        test.SetTrainTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets_MG.root"])
                else:
                        test.SetTrainTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets.root"])
        #test.SetWeight_Sig("weight")
        #test.SetWeight_Bkg("weight")
        test.SetWeight_Sig("1.")
        test.SetWeight_Bkg("1.")
        test.SetNepoch(nepoch)
        test.SetBatchSize(batchsize)
        test.SetTransform(transform)
        test.SetOutputName(name+".root")
        test.Run()
