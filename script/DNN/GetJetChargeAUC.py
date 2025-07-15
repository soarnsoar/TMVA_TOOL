import ROOT
tfile=ROOT.TFile.Open("hists.root")

h_sig=tfile.Get("sig")
h_bkg=tfile.Get("bkg")


total_sig=h_sig.Integral()
total_bkg=h_bkg.Integral()


N=h_sig.GetNbinsX()+1
#dx=(h_sig.GetBinLowEdge(N+1)-h_sig.GetBinLowEdge(1))/N
old_sig_eff=1
AUC=0.
for i in range(N):
    x=h_sig.GetBinLowEdge(i)
    if x> 1: continue
    if x< 0: continue
    this_sig=h_sig.Integral(i,N+1)
    this_bkg=h_bkg.Integral(i,N+1)
    sig_eff=this_sig/total_sig
    bkg_eff=this_bkg/total_bkg
    bkg_rej=1-bkg_eff
    #print bkg_rej
    dx=old_sig_eff-sig_eff
    AUC+=dx*bkg_rej
    old_sig_eff=sig_eff
tfile.Close()

print AUC
