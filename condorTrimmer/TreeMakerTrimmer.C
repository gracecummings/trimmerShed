#define TreeMakerTrimmer_cxx
#include "TreeMakerTrimmer.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>

void TreeMakerTrimmer::Loop(std::string outputFileName)
{
//   In a ROOT session, you can do:
//      root> .L TreeMakerTrimmer.C
//      root> TreeMakerTrimmer t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t nbytes = 0, nb = 0;
   Long64_t original_nentries;

   //counters
   int passEvents = 0;
   int passfilreq = 0;
   int passZreq = 0;
   int passfatreq = 0;
   int passfilandfat = 0;
   int passfilandz = 0;

   //Define the skim output file and tree
   TFile* trimFile = new TFile(outputFileName.c_str(),"recreate");
   TTree* trimTree = fChain->CloneTree(0);
   TH1F*  hnevents = new TH1F("hnevents","original entries",1,0,1);
   TH1F*  hpassfilter = new TH1F("hpassfilter","passing the filters",1,0,1);
   TH1F*  hpassZ = new TH1F("hpassZ","passing the Z req",1,0,1);
   TH1F*  hpassfat = new TH1F("hpassfat","passing the fat jet num",1,0,1);
   TH1F*  hpassfilandfat = new TH1F("hpassfilandfat","passing the filter and fat jet",1,0,1);
   TH1F*  hpassfilandz = new TH1F("hpassfilandz","passing the filter and z",1,0,1);
   TH1F*  hpassall = new TH1F("hpassall","passing all req",1,0,1);
   hnevents->SetBinContent(1,nentries);

   //Branch Handling
   fChain->SetBranchStatus("*",0);
   fChain->SetBranchStatus("ZCandidates",1);
   fChain->SetBranchStatus("JetsAK8Clean",1);
   fChain->SetBranchStatus("HBHEIsoNoiseFilter",1);
   fChain->SetBranchStatus("HBHENoiseFilter",1);
   fChain->SetBranchStatus("globalSuperTightHalo2016Filter",1);
   fChain->SetBranchStatus("EcalDeadCellTriggerPrimitiveFilter",1);
   fChain->SetBranchStatus("BadPFMuonFilter",1);


   //Begin the Skim
   std::cout<<"Starting skim"<<std::endl;

   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;

      //Define bools for events to save
      bool passFilters = false;
      bool passZ = false;
      bool passH = false;
      bool passMET = false;
      bool passfatnum = false;

      //counter for sanity check
      if (jentry%250000==0) {
	std::cout<<"skimming event "<<jentry<<std::endl;
      }
      
      //debug
      //if (jentry == 2000) {
      //break;
      //}

      //filter check
      //First filters for both MC and Data
      if (HBHEIsoNoiseFilter && HBHENoiseFilter && globalSuperTightHalo2016Filter && EcalDeadCellTriggerPrimitiveFilter && BadPFMuonFilter) {
	passFilters = true;
	passfilreq += 1;
      }
      
      //Z Producer Check
      unsigned int nZs = ZCandidates->size();
      if (nZs > 0){
	passZ = true;
	passZreq += 1;
	if (passFilters){
	  passfilandz += 1;
	}
      }

      //Fat Jet checker
      unsigned int nFats = JetsAK8Clean->size();
      if (nFats > 0) {
	passfatnum = true;
	passfatreq += 1;
	if (passFilters){
	  passfilandfat += 1;
	}
      }

      if (Cut(ientry) < 0) continue;
      if (passZ && passfatnum && passFilters) {
      	trimTree->Fill();
      	passEvents += 1;
      }
   }
   hpassfilter->SetBinContent(1,passfilreq);
   hpassZ->SetBinContent(1,passZreq);
   hpassfat->SetBinContent(1,passfatreq);
   hpassall->SetBinContent(1,passEvents);
   hpassfilandfat->SetBinContent(1,passfilandfat);
   hpassfilandz->SetBinContent(1,passfilandz);

   trimFile->Write();
   trimFile->Close();   
   std::cout<<"trimmed to "<< passEvents <<" events"<<std::endl;
   std::cout<<"filter pass "<< passfilreq <<" events"<<std::endl;
   std::cout<<"Z      pass "<< passZreq <<" events"<<std::endl;
   std::cout<<"fat   pass "<< passfatreq <<" events"<<std::endl;
}


  
