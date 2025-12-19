#bmuon_var=["bmuon_nsip3d<10. ? bmuon_nsip3d : 10.","bmuon_reliso","bmuon_ptwrtbjet","bmuon_P_jetrest","bmuon_palongjet < 100 ? bmuon_palongjet : 100","bjet_charge*bmuon_charge"]
bmuon_var=["bmuon_nsip3d<10. ? bmuon_nsip3d : 10.","bmuon_reliso","bmuon_ptwrtbjet < 10. ? bmuon_ptwrtbjet : 10.","bmuon_P_jetrest < 10. ? bmuon_P_jetrest : 10.","bmuon_palongjet < 100. ? bmuon_palongjet : 100.", "bmuon_palongjetratio < 1. ? bmuon_palongjetratio : 1." , "bjet_charge*bmuon_charge", ]

#belectron_var=["belectron_nsip3d < 30. ? belectron_nsip3d : 30.","belectron_reliso","belectron_ptwrtbjet","belectron_P_jetrest","belectron_palongjet < 100 ? belectron_palongjet : 100","bjet_charge*belectron_charge"]

belectron_var=["belectron_nsip3d < 30. ? belectron_nsip3d : 30.","belectron_reliso","belectron_ptwrtbjet < 10. ? belectron_ptwrtbjet : 10.","belectron_P_jetrest < 10. ? belectron_P_jetrest : 10.","belectron_palongjet < 100. ? belectron_palongjet : 100.","belectron_palongjetratio < 1. ? belectron_palongjetratio : 1.","bjet_charge*belectron_charge"]

bjet_var=["bjet_ChargedHadronEnergyFraction","bjet_NeutralHadronEnergyFraction","bjet_NeutralEmEnergyFraction","bjet_ChargedEmEnergyFraction","bjet_MuonEnergyFraction","bjet_ChargedMultiplicity","bjet_NeutralMultiplicity","fabs(bjet_charge)"]
