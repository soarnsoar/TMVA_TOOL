#bmuon_sigcut="(bmuon_charge*bjet_partonFlavour < 0)&&Has_bMuon&&(bmuon_palongjetratio<1.)&&(!TMath::IsNaN(bmuon_P_jetrest))"
#bmuon_bkgcut="(bmuon_charge*bjet_partonFlavour > 0)&&Has_bMuon&&(bmuon_palongjetratio<1.)&&(!TMath::IsNaN(bmuon_P_jetrest))"
#belectron_sigcut="(belectron_charge*bjet_partonFlavour < 0)&&(Has_bElectron)&&(belectron_palongjetratio<1.)&&(!TMath::IsNaN(belectron_P_jetrest))"
#belectron_bkgcut="(belectron_charge*bjet_partonFlavour > 0)&&(Has_bElectron)&&(belectron_palongjetratio<1.)&&(!TMath::IsNaN(belectron_P_jetrest))"

#bmuon_sigcut="(bmuon_charge*bjet_partonFlavour < 0)&&Has_bMuon &&(bmuon_P_jetrest < 10) &&(bmuon_ptwrtbjet<10) && (bmuon_reltrkiso < 10) && (bmuon_palongjetratio < 1) && (bmuon_pt < 100)"
#bmuon_bkgcut="(bmuon_charge*bjet_partonFlavour > 0)&&Has_bMuon &&(bmuon_P_jetrest < 10) &&(bmuon_ptwrtbjet<10) && (bmuon_reltrkiso < 10) && (bmuon_palongjetratio < 1) && (bmuon_pt < 100)"
#belectron_sigcut="(belectron_charge*bjet_partonFlavour < 0)&&(Has_bElectron) && (belectron_ptwrtbjet < 10) && (belectron_P_jetrest < 10) && (belectron_palongjetratio < 1) && (belectron_pt < 100)"
#belectron_bkgcut="(belectron_charge*bjet_partonFlavour > 0)&&(Has_bElectron) && (belectron_ptwrtbjet < 10) && (belectron_P_jetrest < 10) && (belectron_palongjetratio < 1) && (belectron_pt < 100)"


bmuon_sigcut="(bmuon_charge*bjet_partonFlavour < 0)&&Has_bMuon"
bmuon_bkgcut="(bmuon_charge*bjet_partonFlavour > 0)&&Has_bMuon"
belectron_sigcut="(belectron_charge*bjet_partonFlavour < 0)&&(Has_bElectron)"
belectron_bkgcut="(belectron_charge*bjet_partonFlavour > 0)&&(Has_bElectron)"


bjet_sigcut="(bjet_charge*bjet_partonFlavour < 0)&&(!Has_bElectron)&&(!Has_bMuon)"
bjet_bkgcut="(bjet_charge*bjet_partonFlavour > 0)&&(!Has_bElectron)&&(!Has_bMuon)"
