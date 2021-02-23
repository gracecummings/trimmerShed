import argparse
import glob
import os

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--fname",type=str)
    args = parser.parse_args()

    sampstrend = args.fname.split("samplesToSkim_2018_")[-1]
    sampstr    = sampstrend.split(".txt")[0]
    fchecknames = glob.glob("../../../../../TreeMakerGarden/CMSSW_10_2_21/src/TreeMaker/Production/python/Autumn18/"+sampstr+"*")
    fcheck = open(fchecknames[0],"r")
    fcheckl = fcheck.readlines()
    numberfiles = 0
    nstrl = []
    for l,line in enumerate(fcheckl):
        if sampstr in line:
            numberfiles += 1
            nstrl.append(str(numberfiles-1))

    nstrl.sort()
    print "Number of files in config: ",numberfiles


    f = open(args.fname,"r")
    fl = f.readlines()
    fl.sort(key = lambda x:x.split('pythia8_')[-1].split("_RA")[0])
    flnums = [x.split('pythia8_')[-1].split("_RA")[0] for x in fl]

    print "Number of files produced: ",len(fl)
    
    settrue = set(nstrl)
    setmade = set(flnums)

    setmiss = settrue-setmade

    print "missing files: ",setmiss

    for val in setmiss:
        jdlName = "missedsub_"+sampstr+"_"+val+".jdl"
        jdl = open(jdlName,"w")
        jdl.write("universe = vanilla\n")
        jdl.write("Executable = jobExecCondor.sh\n")
        jdl.write('+REQUIRED_OS = "rhel7"\n')
        jdl.write("request_disk = 1000000\n")
        jdl.write("request_memory = 3500\n")
        jdl.write("request_cpus = 1\n")
        jdl.write("Should_Transfer_Files = YES\n")
        jdl.write("WhenToTransferOutput = ON_EXIT_OR_EVICT\n")
        jdl.write("Transfer_Input_Files = jobExecCondor.sh, step1.sh,step2.sh, CMSSW_10_2_21.tar.gz, input/args_Autumn18."+sampstr+"_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_"+val+".txt\n")
        jdl.write("Output = resubOut/{0}_{1}_{2}_out.stdout\n".format("Autumn18."+sampstr+"_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",val,"missed"))
        jdl.write("Error = resubOut/{0}_{1}_{2}_err.stder\n".format("Autumn18."+sampstr+"_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",val,"missed"))
        jdl.write("Log = resubOut/{0}_{1}_{2}_log.log\n".format("Autumn18."+sampstr,val,"missed"))
        jdl.write("Arguments = -S step1.sh,step2.sh -C CMSSW_10_2_21 -j {0} -p {1} -o root://cmseos.fnal.gov//store/group/lpcboostres/dyjets2018_feb2021_missed\n".format("Autumn18."+sampstr+"_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8",val))
        jdl.write("want_graceful_removal = true\n")
        jdl.write("on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)\n")
        jdl.write("on_exit_hold = ( (ExitBySignal == True) || (ExitCode != 0) )\n")
        jdl.write("\n")
        jdl.write("Queue 1\n")#Not sure about this one
        jdl.close()
        #os.system("condor_submit {0}".format(jdlName))
        
