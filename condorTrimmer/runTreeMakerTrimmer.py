import ROOT
import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("-s","--inputSampleDirandName",type=str)works with just skimming by sample or file, not chunking
    parser.add_argument("-f","--fileList",type=str)
    parser.add_argument("-e","--eosDirName",type=str)
    parser.add_argument("-o","--outPutFile",type=str)
    args = parser.parse_args()

    #Get the files you want skimmed
    filesToSkimraw = args.fileList
    #filesToSkim = args.fileList
    #filesToSkim    = filesToSkimraw.strip("[]").split("'")#Converts string into list
    filesToSkim    = filesToSkimraw.strip("[]").split(",")#Converts string into list
    filesToSkim     = list(map(lambda x:x.strip("''"),filesToSkim))
    eosFileLocal = args.eosDirName 
    #sampleToSkim  = args.inputSampleDirandName
    #samplePath    = "root://cmseos.fnal.gov//store/user/gcumming/"+sampleToSkim+"*_RA2AnalysisTree.root/TreeMaker2/PreSelection"#this one takes all files that match the sample, corrupts when large
    #samplePath    = "root://cmseos.fnal.gov//store/user/gcumming/"+sampleToSkim+"/TreeMaker2/PreSelection"#this takes each file indivdually, makes a fuck ton of jobs

    #Print statements for directions
    #print "Skim to be saved in ",eosFileLocal
    print "Raw list of files to skim: "
    #print filesToSkimraw
    #print "List of files to skim: ",filesToSkim
    #print "    type of list ",type(filesToSkim)
    #print "    type of element ",type(filesToSkim[0])
    print "file path: root://cmseos.fnal.gov//store/user/"+eosFileLocal+"/"
    print "file will be saved undername ",args.outPutFile

    print "Skimming {0} trees starting with:".format(len(filesToSkim))
    print "    ",filesToSkim[0]

    #Make the TChain
    inChain = ROOT.TChain("PreSelection")
    for f in filesToSkim:
        inChain.Add("root://cmseos.fnal.gov//store/user/"+eosFileLocal+"/"+f+"/TreeMaker2/PreSelection")
        #inChain.Add(f+"/TreeMaker2/PreSelection")
    eventsToSkim = inChain.GetEntries()
    print "you are going to skim {0} events".format(eventsToSkim)

    #Make the output file that holds the skimmed events
    outFileName = args.outPutFile
    outFile     = outFileName+"_skim_"+str(eventsToSkim)+"MiniAODEvents.root"#For condor

    #Compile the macro to do the skimming
    ROOT.gSystem.CompileMacro("TreeMakerTrimmer.C","g0ck")
    ROOT.gSystem.Load('TreeMakerTrimmer_C')
    trimmer = ROOT.TreeMakerTrimmer(inChain)
    trimmer.Loop(outFile)

    print "congrats, you have made a skim. Hope it is lean enough for you."
    
    
