import os
maindir=os.getenv("JH_TMVA_TOOL_MAINDIR")
curdir=os.getcwd()
def GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO):
    nlayer=str(nlayer)
    nnode=str(nnode)
    batchsize=str(batchsize)
    dropout=str(dropout)
    version=str(version)
    year=str(year)
    nepoch=str(nepoch)
    ret="--name "+name+" --nlayer "+nlayer+" --nnode "+nnode+" --batchsize "+batchsize+" --dropout "+dropout+" --nepoch "+nepoch+" --version "+version+" --channel "+channel+" --year "+year+" --analyzer "+analyzer+" --transform "+transform
    if switch: ret+=" --switch"
    if useLO: ret+=" --useLO"
    return ret
def MakeCommand(workdir,name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO):
    commandlist=[
        "cd "+curdir,
        "cd "+workdir,
        "python "+maindir+"/script/run_single.py "+GetOptionCommand(name,nlayer,nnode,batchsize,dropout,nepoch,version,channel,switch,year,analyzer,transform,useLO),
        ]
    ret="&&".join(commandlist)
    return ret
