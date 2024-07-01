year=2016preVFP

(mkdir -p muon${year}&&       cd muon${year} &&   run_N_1.py --nlayer 5 --name muon_test     --nnode 64 --nepoch 300 --batchsize 500 --dropout 0.2 --version 2405.4 --channel muon     --year $year --analyzer EEMu_MuMuE_Method --transform G --auc_cut 0.75 && cd -) &> muon_$year.log&
(mkdir -p electron${year} && cd electron${year} &&run_N_1.py --nlayer 5 --name electron_test --nnode 64 --nepoch 300 --batchsize 500 --dropout 0.2 --version 2405.4 --channel electron --year $year --analyzer EEMu_MuMuE_Method --transform G --auc_cut 0.7 && cd -) &> electron_$year.log&
(mkdir -p jet${year} && cd jet${year} && run_N_1.py --nlayer 3 --name jet_test --nnode 50 --nepoch 300 --batchsize 100 --dropout 0.1 --version 2405.4 --channel jet --year $year --analyzer EEMu_MuMuE_Method --transform "N,G" --auc_cut 0.59 && cd -) &> jet_$year.log&


