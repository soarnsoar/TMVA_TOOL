import ROOT
import os
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
inputfile=maindir+"/inputs/EEMu_MuMuE_Method/v2405.4/2017/EEMu_MuMuE_Method_DYJets.root"

tfile=ROOT.TFile.Open(inputfile)
tree_sig=tfile.Get("OutTree/sig")
tree_bkg=tfile.Get("OutTree/bkg")
#bjet_charge

h_sig=ROOT.TH1D("sig","sig",1000,-0.1,1.1)
h_bkg=ROOT.TH1D("bkg","bkg",1000,-0.1,1.1)


for event in tree_sig:
    h_sig.Fill(abs(event.bjet_charge))
for event in tree_bkg:
    h_bkg.Fill(abs(event.bjet_charge))



f_out=ROOT.TFile("hists.root","RECREATE")
h_sig.Write()
h_bkg.Write()
f_out.Close()

tfile.Close()
