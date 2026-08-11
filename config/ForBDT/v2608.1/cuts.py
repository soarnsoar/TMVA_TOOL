bmuon_sigcut="(bmuon_charge*bjet_partonFlavour < 0)&&Has_bMuon"
bmuon_bkgcut="(bmuon_charge*bjet_partonFlavour > 0)&&Has_bMuon"
belectron_sigcut="(belectron_charge*bjet_partonFlavour < 0)&&(Has_bElectron)"
belectron_bkgcut="(belectron_charge*bjet_partonFlavour > 0)&&(Has_bElectron)"


bjet_sigcut="(bjet_charge*bjet_partonFlavour < 0)&&(!Has_bElectron)&&(!Has_bMuon)"
bjet_bkgcut="(bjet_charge*bjet_partonFlavour > 0)&&(!Has_bElectron)&&(!Has_bMuon)"
