from ExportShellCondorSetup_tamsa import Export
import os
#def Export(WORKDIR,command,jobname,submit,ncpu,memory=False,nretry=3):

list_obj=["muon","electron","jet"]
list_year=["2016preVFP","2016postVFP","2017","2018"]
list_transform=['D', 'G', 'I', 'N', 'P', 'U']
for year in list_year:
    for obj in list_obj:
        for transform in list_transform:
            workdir="WORKDIR_PICKLE/"+obj+"__"+year+"__"+transform+"/"
            thisdir=os.getcwd()
            #this_obj=sys.argv[1]
            #this_year=sys.argv[2]
            #this_transform=sys.argv[3]
            #RunYear(this_obj,this_year)
            command="cd "+thisdir+"&&python3 parse_results_export_to_pickle.py "+obj+" "+year+" "+transform
            jobname="parsing "+obj+year
            submit=1
            ncpu=1
            Export(workdir,command,jobname,submit,ncpu)
