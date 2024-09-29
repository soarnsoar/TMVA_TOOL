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
        _nlayer=dict_options["nlayer"]
        _nnode=dict_options["nnode"]
        _nepoch=dict_options["nepoch"]
        _batchsize=dict_options["batchsize"]
        _dropout=dict_options["dropout"]
        _name=dict_options["name"]
        _version=dict_options["version"]
        _channel=dict_options["channel"]
        _analyzer=dict_options["analyzer"]
        _year=dict_options["year"]
        _transform=dict_options["transform"]
        _bmuon_var=dict_options["bmuon_var"]
        _belectron_var=dict_options["belectron_var"]
        _bjet_var=dict_options["bjet_var"]
        _bmuon_sigcut=dict_options["bmuon_sigcut"]
        _bmuon_bkgcut=dict_options["bmuon_bkgcut"]
        _belectron_sigcut=dict_options["belectron_sigcut"]
        _belectron_bkgcut=dict_options["belectron_bkgcut"]
        _bjet_sigcut=dict_options["bjet_sigcut"]
        _bjet_bkgcut=dict_options["bjet_bkgcut"]

        ##--[END]read options


        _variables=[]




        _sigcut=""
        _bkgcut=""
        if _channel=="muon":
                _variables=_bmuon_var+_bjet_var
                for v in skiplist:
                        if v in _variables:
                                _variables.remove(v)
                _sigcut=_bmuon_sigcut
                _bkgcut=_bmuon_bkgcut
                
        elif _channel=="electron":
                _variables=_belectron_var+_bjet_var
                for v in skiplist:
                        if v in _variables:
                                _variables.remove(v)
                _sigcut=_belectron_sigcut
                _bkgcut=_belectron_bkgcut
        elif _channel=="jet":
                _variables=_bjet_var+[] ##avoid ref.
                for v in skiplist:
                        if v in _variables:
                                _variables.remove(v)
                _sigcut=_bjet_sigcut
                _bkgcut=_bjet_bkgcut
        else:
                print "[run_nnode_nlayer_nepoch_batchsize.py]Wrong _channel input",_channel
                1/0
        print "sigcut->",_sigcut
        print "bkgcut->",_bkgcut


        from TMVA_DNN import TMVA_DNN_TOOL
        test=TMVA_DNN_TOOL()
        test.SetFactoryName(_name)
        test.SetInputVariables(_variables)
        #test.SetSpectators(["bjet_partonFlavour","lhe_b_pdgid","bjet_partonFlavour*lhe_b_pdgid>0","bmuon_charge","belectron_charge","bjet_charge"])
        test.SetSpectators([])
        
        test.SetCut_Sig(_sigcut)
        test.SetCut_Bkg(_bkgcut)
        test.SetNlayer(_nlayer)
        test.SetNnode(_nnode)
        test.SetDropout(_dropout)



        test.SetTestTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+_analyzer+"/v"+_version+"/"+_year+"/"+_analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+_analyzer+"/v"+_version+"/"+_year+"/"+_analyzer+"_DYJetsToMuMu_MiNNLO.root"])
        test.SetTrainTreeAndInput_Sig("OutTree/sig",[maindir+"/inputs/"+_analyzer+"/v"+_version+"/"+_year+"/"+_analyzer+"_DYJets.root"])
        test.SetTestTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+_analyzer+"/v"+_version+"/"+_year+"/"+_analyzer+"_DYJetsToEE_MiNNLO.root",maindir+"/inputs/"+_analyzer+"/v"+_version+"/"+_year+"/"+_analyzer+"_DYJetsToMuMu_MiNNLO.root"])
                
        test.SetTrainTreeAndInput_Bkg("OutTree/bkg",[maindir+"/inputs/"+_analyzer+"/v"+_version+"/"+_year+"/"+_analyzer+"_DYJets.root"])
        #test.SetWeight_Sig("weight")
        #test.SetWeight_Bkg("weight")
        test.SetWeight_Sig("1.")
        test.SetWeight_Bkg("1.")
        test.SetNepoch(_nepoch)
        test.SetBatchSize(_batchsize)
        test.SetTransform(_transform)
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
        parser.add_argument('--ntrial', dest='ntrial_cut', default=4, help="if it drops AUC, try more indep. trainings")        

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
        ntrial_cut=int(args.ntrial_cut)
        #skiplist=[]
        #if args.skiplist!=None:
        #        skiplist=args.skiplist.split(',')




        bmuon_var,belectron_var,bjet_var=GetVariableConfig(version)


        testlist=[]
        auc_cut=float(args.auc_cut)

        if auc_cut<0:
                print "----Get AUC Cut"
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
                        "bjet_bkgcut":bjet_bkgcut,

                }
                skiplist=[]
                this_auc=RunWithoutList(skiplist,dict_options)
                print this_auc
                print "Set the AUC cut->",this_auc
                auc_cut=this_auc




        if channel=="muon":
                testlist=bmuon_var+bjet_var

        if channel=="electron":
                testlist=belectron_var+bjet_var

        if channel=="jet":
                testlist=bjet_var+[] ## to avoid being a pointer

        print "--testlist--"
        print testlist
        rmlist=[]
        for iv,v in enumerate(testlist):
                print iv,v


        for iv,v in enumerate(testlist):
                print "-->>Check testlist"
                print testlist
                print iv,v
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
                        "bjet_bkgcut":bjet_bkgcut,

                }
                ntrial=1
                SkipThis=0
                while ntrial < ntrial_cut:
                        this_auc=RunWithoutList(skiplist,dict_options)
                        print this_auc
                        SkipThis=this_auc>auc_cut
                        if SkipThis: ## not drop the AUC
                                break
                        else:
                                print "this variable",v,"drops the AUC for Trial#==",ntrial
                                ntrial+=1

                if SkipThis:
                        print v,"does NOT drop AUC. we don't need it"
                        print "no ",v,"-->AUC=",this_auc
                        print "AUC cut=",auc_cut
                        rmlist.append(v)
                else:
                        print v," DROP AUC. we need it. Don't remove it from input variable list"
                        print "no ",v,"-->AUC=",this_auc
                        print "AUC cut=",auc_cut
                        

        print "testlist=>",testlist
        print "rmlist=>",rmlist


