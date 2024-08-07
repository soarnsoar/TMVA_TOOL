#### use cvmfs for root ####                                                                                                      
#/cvmfs/cms.cern.ch/el8_amd64_gcc10/cms/cmssw/CMSSW_12_3_4
export CMS_PATH=/cvmfs/cms.cern.ch
source $CMS_PATH/cmsset_default.sh
#export SCRAM_ARCH=slc7_amd64_gcc900
#export SCRAM_ARCH=slc7_amd64_gcc820
export SCRAM_ARCH=el8_amd64_gcc10
#export cmsswrel='cmssw/CMSSW_10_6_4'
export cmsswrel='cmssw/CMSSW_12_3_4'

cd /cvmfs/cms.cern.ch/$SCRAM_ARCH/cms/$cmsswrel/src
echo "@@@@ SCRAM_ARCH = "$SCRAM_ARCH
echo "@@@@ cmsswrel = "$cmsswrel
echo "@@@@ scram..."
eval `scramv1 runtime -sh`
cd -
source /cvmfs/cms.cern.ch/$SCRAM_ARCH/cms/$cmsswrel/external/$SCRAM_ARCH/bin/thisroot.sh
