bmuon_var=[
    "bmuon_dR_l_j",
    "bmuon_nsip3d > 10. ? 10. : bmuon_nsip3d",
    "bmuon_P_jetrest < 1. ? 1. : bmuon_P_jetrest > 4. ? 4. : bmuon_P_jetrest",
    "bmuon_palongjet > 10. ? 10. : bmuon_palongjet",
    "bmuon_palongjetratio > 0.4 ? 0.4 : bmuon_palongjetratio",
    "bmuon_ptwrtbjet > 3. ? 3. : bmuon_ptwrtbjet",
    #"bmuon_reliso > 6 ? 6 : bmuon_reliso",
    "log10(1.+bmuon_reliso) > 1.2 ? 1.2 : log10(1.+bmuon_reliso)",
    "bjet_ChargedHadronEnergyFraction < 0.2 ? 0.2 : bjet_ChargedHadronEnergyFraction > 0.9 ? 0.9 : bjet_ChargedHadronEnergyFraction",
    #"bjet_ChargedMultiplicity > 20 ? 20 : bjet_ChargedMultiplicity",
    "bjet_MuonEnergyFraction < 0.2 ? 0.2 : bjet_MuonEnergyFraction > 0.4 ? 0.4 : bjet_MuonEnergyFraction",
    "bjet_NeutralEmEnergyFraction > 0.5 ? 0.5 : bjet_NeutralEmEnergyFraction",
    "bjet_NeutralHadronEnergyFraction < 0.1 ? 0.1 : bjet_NeutralHadronEnergyFraction > 0.3 ? 0.3 : bjet_NeutralHadronEnergyFraction",
    "bjet_NeutralMultiplicity > 25 ? 25 : bjet_NeutralMultiplicity",
    "bjet_charge*bmuon_charge < -0.3 ? -0.3 : bjet_charge*bmuon_charge > 0.5 ? 0.5 : bjet_charge*bmuon_charge",
    "fabs(bjet_charge) > 0.5 ? 0.5 : fabs(bjet_charge)"
    
]

belectron_var=[
    "belectron_dR_l_j < 0.13 ? 0.13 : belectron_dR_l_j",
    "belectron_nsip3d > 10. ? 10. : belectron_nsip3d",
    "belectron_P_jetrest > 2. ? 2. : belectron_P_jetrest",
    "belectron_palongjet > 15.? 15. : belectron_palongjet",
    "belectron_palongjetratio > 0.2 ? 0.2 : belectron_palongjetratio",
    "belectron_ptwrtbjet > 3. ? 3. : belectron_ptwrtbjet",
    #"belectron_reliso < 1.5 ? 1.5 : belectron_reliso > 6 ? 6 : belectron_reliso",
    "log10(1.+belectron_reliso) > 1.1 ? 1.1 : log10(1.+belectron_reliso)",

    "bjet_ChargedEmEnergyFraction > 0.2 ? 0.2 : bjet_ChargedEmEnergyFraction",
    "bjet_ChargedHadronEnergyFraction < 0.5 ? 0.5 : bjet_ChargedHadronEnergyFraction",
    "bjet_NeutralEmEnergyFraction < 0.15 ? 0.15 : bjet_NeutralEmEnergyFraction > 0.6 ? 0.6 : bjet_NeutralEmEnergyFraction",
    "bjet_NeutralMultiplicity",

    "bjet_charge*belectron_charge < -0.4 ? -0.4 : bjet_charge*belectron_charge > 0.2 ? 0.2 : bjet_charge*belectron_charge",
    "fabs(bjet_charge) > 0.35 ? 0.35 : fabs(bjet_charge)",
]

bjet_var=[
    "bjet_ChargedHadronEnergyFraction < 0.2 ? 0.2 : bjet_ChargedHadronEnergyFraction",
    #"bjet_ChargedMultiplicity > 30 ? 30 : bjet_ChargedMultiplicity",
    "bjet_NeutralEmEnergyFraction > 0.7 ? 0.7 : bjet_NeutralEmEnergyFraction",
    "bjet_NeutralHadronEnergyFraction > 0.4 ? 0.4 : bjet_NeutralHadronEnergyFraction",
    "bjet_NeutralMultiplicity > 30 ? 30 : bjet_NeutralMultiplicity",
    "fabs(bjet_charge) > 0.4 ? 0.4 : fabs(bjet_charge)"   
]
