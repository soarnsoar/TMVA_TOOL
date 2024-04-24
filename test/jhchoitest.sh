#        parser.add_argument('--nlayer', dest='nlayer', default="5", help="nlayyer")
#        parser.add_argument('--name', dest='name', default="dnn", help="name")
#        parser.add_argument('--nnode', dest='nnode', default="128", help="nnode")
#        parser.add_argument('--nepoch', dest='nepoch', default="300", help="nepoch")
#        parser.add_argument('--batchsize', dest='batchsize', default="1000", help="batchsize")
#        parser.add_argument('--dropout', dest='dropout', default="0.2", help="dropout")
#        parser.add_argument('--version', dest='version', default="1.0", help="version")
#        parser.add_argument('--channel', dest='channel', default="-", help="muon/electron/jet")
nlayer=5
nnode=128
nepoch=100
batchsize=3000
dropout=0.2
version=1.0
channel=muon
name="test"
run_single.py --nlayer ${nlayer} --name ${name} --nnode ${nnode} --nepoch ${nepoch} --batchsize ${batchsize} --dropout ${dropout} --version ${version} --channel ${channel}
