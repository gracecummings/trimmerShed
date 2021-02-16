 #Author: Grace Cummings
#Date: November 13th, 2019
#Purpose: Script to generate jdl files for condor submissions of the skimmer script
#Notes: Based on scripts by B. Tannenwald https://github.com/neu-physics/BsToMuMuAnalysis/blob/master/submitSampleToCondor.py and J. Hakala https://gitlab.cern.ch/johakala/nanolyzer/blob/condor/generateJobs.py


import os
import sys
import argparse
from datetime import date
from itertools import islice

parser = argparse.ArgumentParser()
parser.add_argument("-s","--sampleTXTFile",help=".txt file with the ntuple names you want skimmed")
parser.add_argument("-e","--eosDirTuples",help="path to ntuples in /store/user/")
parser.add_argument("-d","--prodDate",help="date when ntuples were made exp 'Nov12'")
parser.add_argument("-c","--chunksize",type=int,help="how many files you want to run over per job")
args = parser.parse_args()

#eosDirName = "skims"+str(args.prodDate)

#Check input text file
if (args.sampleTXTFile is None):
    print "please specify path to text file with samples to be skimmed"
else:
    if (not os.path.exists(args.sampleTXTFile)):
        print "invalid sample text file"
    name1 = str(args.sampleTXTFile).split("samplesToSkim_")[-1]
    nameSamp = name1.split(".txt")[0]
    eosDirName = nameSamp+"_"+str(date.today())

#Make log directories
if not os.path.exists("condorTrimmerOutput/"+str(date.today())+"/"):
    os.makedirs("condorTrimmerOutput/"+str(date.today())+"/")

#Tar the work area
print "Creating tarball of work area"
tarballName = "condorTrimmer.tar.gz"
os.system("tar -h -cvf "+tarballName+" condorTrimmer")


#Create jobs
txtFile = open(args.sampleTXTFile,"r")
readIn  = txtFile.readlines()
corrIn  = map(lambda x : x.split("\n")[0],readIn)
corrInstr = str(corrIn)
corrInstr = corrInstr.replace(' ','')

#chunking
filenum = len(corrIn)
cleanDiv = filenum/args.chunksize
remain   = filenum % args.chunksize
chunks = []
if remain != 0:
    chunks = [args.chunksize]*cleanDiv+[remain]
else:
    chunks = [args.chunksize]*cleanDiv
iterIn = iter(corrIn)
chunkedIn = [list(islice(iterIn,elem)) for elem in chunks]
nchunks = len(chunkedIn)
print "Number of chunks: ",nchunks

for i,chunk in enumerate(chunkedIn):
    sampleName = chunk[0].split("_RA")[0]#Only works with chunking
    samplePath = str(args.eosDirTuples)+'/'+sampleName

    #Make the jdl for each sample
    jdlName = "trimmer_"+sampleName+"_chunk"+str(i)+"_"+str(date.today())+".jdl"
    jdl = open(jdlName,"w")
    jdl.write("universe = vanilla\n")
    jdl.write("Should_Transfer_Files = YES\n")
    jdl.write("WhenToTransferOutput = ON_EXIT\n")
    jdl.write("Transfer_Input_Files = "+tarballName+"\n")
    jdl.write("Output = condorTrimmerOutput/{0}/{1}_out.stdout\n".format(str(date.today()),sampleName+"_chunk"+str(i)))
    jdl.write("Error = condorTrimmerOutput/{0}/{1}_err.stder\n".format(str(date.today()),sampleName+"_chunk"+str(i)))
    jdl.write("Log = condorTrimmerOutput/{0}/{1}_log.log\n".format(str(date.today()),sampleName+"_chunk"+str(i)))
    jdl.write("Executable = trimmer.sh\n")
    good_chunk = str(chunk).replace(' ','')#This id the string I need to pass to 
    test_chunk = str(chunk).translate(None,' ')
    jdl.write("Arguments = {0} {1} {2} {3} {4} {5}\n".format(args.eosDirTuples,sampleName+"_chunk"+str(i)+"_",eosDirName,good_chunk),str(i),str(nchunks))
    jdl.write('+DESIRED_Sites="T3_US_Baylor,T2_US_Caltech,T3_US_Colorado,T3_US_Cornell,T3_US_FIT,T1_US_FNAL,T3_US_FNALLPC,T3_US_Omaha,T3_US_JHU,T3_US_Kansas,T2_US_MIT,T3_US_NotreDame,T2_US_Nebraska,T3_US_NU,T3_US_OSU,T3_US_Princeton_ICSE,T2_US_Purdue,T3_US_Rice,T3_US_Rutgers,T3_US_MIT,T3_US_NERSC,T3_US_SDSC,T3_US_FIU,T3_US_FSU,T3_US_OSG,T3_US_TAMU,T3_US_TTU,T3_US_UCD,T3_US_UCSB,T2_US_UCSD,T3_US_UMD,T3_US_UMiss,T2_US_Vanderbilt,T2_US_Wisconsin"')
    jdl.write("\n")
    jdl.write("Queue 1\n")#Not sure about this one
    jdl.close()
    #print chunk
    #print good_chunk
    
    #submit the jobs
    #os.system("condor_submit {0}".format(jdlName))
    
