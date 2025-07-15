#!/usr/bin/env python
import ROOT



if __name__== '__main__':
        import argparse
        parser = argparse.ArgumentParser(description='input argument')
        parser.add_argument('-i', dest='input', default="")
        args = parser.parse_args()
        this_input=args.input
        f=ROOT.TFile.Open(this_input)
        keylist=f.GetListOfKeys()

        dirname=""
        for key in keylist:
            classname= key.GetClassName()
            if "TDirectory" in classname:
                    dirname=key.GetName()
        if dirname=="": exit()
        print dirname
        f.Get(dirname+"/Method_DNN/DNN").ls()
