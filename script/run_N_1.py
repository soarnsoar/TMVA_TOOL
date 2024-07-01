#!/usr/bin/env python
##-----
import os
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
def GetVariableConfig(version):
        version=str(version)
	exec(open(maindir+"/config/v"+version+"/variables_rank.py"))
        return bmuon_var,belectron_var,bjet_var
def GetCutConfig(version):
        version=str(version)
	exec(open(maindir+"/config/v"+version+"/cuts.py"))
        return bmuon_sigcut,bmuon_bkgcut,belectron_sigcut,belectron_bkgcut,bjet_sigcut,bjet_bkgcut







def RunWithoutList(skiplist,dict_options):
        print "--SKIP FOLLOWING VARS"
        print skiplist
        ##--read options
        nlayer=dict_options["nlayer"]
        nnode=dict_options["nnode"]
        nepoch=dict_options["nepoch"]
        batchsize=dict_options["batchsize"]
        dropout=dict_options["dropout"]
        name=dict_options["name"]
        version=dict_options["version"]
        channel=dict_options["channel"]
        analyzer=dict_options["analyzer"]
        year=dict_options["year"]
        transform=dict_options["transform"]
        bmuon_var=dict_options["bmuon_var"]
        belectron_var=dict_options["belectron_var"]
        bjet_var=dict_options["bjet_var"]
        bmuon_sigcut=dict_options["bmuon_sigcut"]
        bmuon_bkgcut=dict_options["bmuon_bkgcut"]
        belectron_sigcut=dict_options["belectron_sigcut"]
        belectron_bkgcut=dict_options["belectron_bkgcut"]
        bjet_sigcut=dict_options["bjet_sigcut"]
        bjet_bkgcut=dict_options["bjet_bkgcut"]

        ##--[END]read options


        variables=[]




        sigcut=""
        bkgcut=""
        if channel=="muon":
                variables=bmuon_var+bjet_var
                for v in skiplist:
                        if v in variables:
                                variables.remove(v)
                sigcut=bmuon_sigcut
                bkgcut=bmuon_bkgcut
                
        elif channel=="electron":
                variables=belectron_var+bjet_var
                for v in skiplist:
                        if v in variables:
                                variables.remove(v)
                sigcut=belectron_sigcut
                bkgcut=belectron_bkgcut
        elif channel=="jet":
                variables=bjet_var
                for v in skiplist:
                        if v in variables:
                                variables.remove(v)
                sigcut=bjet_sigcut
                bkgcut=bjet_bkgcut
        else:
                print "[run_nnode_nlayer_nepoch_batchsize.py]Wrong channel input"
                channel
                1/0
        print "sigcut->",sigcut
        print "bkgcut->",bkgcut


        from TMVA_DNN import TMVA_DNN_TOOL
        test=TMVA_DNN_TOOL()
        test.SetFactoryName(name)
        test.SetInputVariables(variables)
        #test.SetSpectators(["bjet_partonFlavour","lhe_b_pdgid","bjet_partonFlavour*lhe_b_pdgid>0","bmuon_charge","belectron_charge","bjet_charge"])
        test.SetSpectators([])
        
        test.SetCut_Sig(sigcut)
        test.SetCut_Bkg(bkgcut)
        test.SetNlayer(nlayer)
        test.SetDropout(dropout)



        test.SetTestTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToMuMu_MiNNLO.root"])
        test.SetTrainTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJets.root"])
        test.SetTestTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+analyzer+"/v"+version+"/"+year+"/"+analyzer+"_DYJetsToMuMu_MiNNLO.root"])
                
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
        _auc=test.GetAUC("DNN")
        del test
        return _auc
        
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



        parser.add_argument('--year', dest='year', default="", help="year")        
        parser.add_argument('--analyzer', dest='analyzer', default="", help="year")        

        parser.add_argument('--transform', dest='transform', default="I", help="transform")        
        parser.add_argument('--auc_cut', dest='auc_cut', default=-1, help="min auc to use")        

        #parser.add_argument('--skiplist', dest='skiplist', default=None, help="Don't use this variable for the training")


        args = parser.parse_args()
        
        nlayer=int(args.nlayer)
        nnode=int(args.nnode)
        nepoch=int(args.nepoch)
        batchsize=int(args.batchsize)
        dropout=float(args.dropout)
        name=args.name
        version=args.version
        channel=args.channel
        

        analyzer=args.analyzer
        year=args.year

        transform=args.transform
        #skiplist=[]
        #if args.skiplist!=None:
        #        skiplist=args.skiplist.split(',')




        bmuon_var,belectron_var,bjet_var=GetVariableConfig(version)


        testlist=[]
        auc_cut=float(args.auc_cut)
        if channel=="muon":
                testlist=bmuon_var+bjet_var
                if auc_cut<0:
                        print "auc_cut is not set. Use default"
                        auc_cut=0.75
        if channel=="electron":
                testlist=belectron_var+bjet_var
                if auc_cut<0:
                        print "auc_cut is not set. Use default"
                        auc_cut=0.72
        if channel=="jet":
                testlist=bjet_var
                if auc_cut<0:
                        print "auc_cut is not set. Use default"
                        auc_cut=0.59
        rmlist=[]
        for v in testlist:
                print "======"
                print "TEST->",v
                skiplist=rmlist+[v]

                bmuon_sigcut,bmuon_bkgcut,belectron_sigcut,belectron_bkgcut,bjet_sigcut,bjet_bkgcut=GetCutConfig(version)

                dict_options={
                        "nlayer":nlayer,
                        "nnode":nnode,
                        "nepoch":nepoch,
                        "batchsize":batchsize,
                        "dropout":dropout,
                        "name":name,
                        "version":version,
                        "channel":channel,
                        "analyzer":analyzer,
                        "year":year,
                        "transform":transform,
                        "bmuon_var":bmuon_var,
                        "belectron_var":belectron_var,
                        "bjet_var":bjet_var,
                        "bmuon_sigcut":bmuon_sigcut,
                        "bmuon_bkgcut":bmuon_bkgcut,
                        "belectron_sigcut":belectron_sigcut,
                        "belectron_bkgcut":belectron_bkgcut,
                        "bjet_sigcut":bjet_sigcut,
                        "bjet_bkgcut":bjet_bkgcut
                }

                this_auc=RunWithoutList(skiplist,dict_options)
                print this_auc
                SkipThis=this_auc>auc_cut
                print "----"
                if SkipThis:
                        print v,"does NOT drop AUC. we don't need it"
                        print "no ",v,"-->AUC=",this_auc
                        print "AUC cut=",auc_cut
                        rmlist.append(v)
                else:
                        print v," DROP AUC. we need it. Don't remove it from input variable list"
                        print "no ",v,"-->AUC=",this_auc
                        print "AUC cut=",auc_cut
                        

        print "rmlist=>",rmlist
