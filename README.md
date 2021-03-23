# trimmerShed

Internalizing the "tree" theme, to skim the TreeMaker ntuples to a more manangeble amount, we have a trimmer, and this repo is the "shed" where you keep it. The trimmer is in its most basic form, and will eventually be combined (hopefully) with the "topiary" step of the analysis, but this has not been added yet. This is the second step in the ZpAnomalon analysis flow. First step is ntuplization, third and subsequent are plotting and high level calculations.

To make the ntuples easier to use, we do a first minimal pass of cuts, requireing a Z Candidate in the event, as well as at least one fat jet. That is all, and this is enough to make the files small enough to run locally. This is batch job recipe, and is currently tested to run on CMS Connect. 

## Setting up the Environment


This trimmer does not require ROOT or CMSSW, just python2 for submission, which is still the default for the CMS Connect submit nodes. You can build the trimmer in your CMS Connect home area, but submissions work better from the scratch area.

```bash
ssh YOURUSERNAME@login-el7.uscms.org
git clone https://github.com/gracecummings/trimmerShed.git
cd /local-scratch/YOURUSERNAME/trimmershed
```

Just download this trimmer in anyway you see fit. Since CMS Connect is a bit demanding with the ssh keys, I just use the https git clone.

##Submitting batch jobs

Submitting the trimmer jobs to the CMS Connect Condor Cluster involves 4 parameters, passed as command line options to `submitTrimmerToCondor.py`:

+ `-s` takes a `.txt` file with the names of the ntuple outfiles. This repo already has `.txt` files with many of the samples prepped, but for custom naming, a new text file would need to be made
+ `-e` is the fnal eos path where the ntuples are stored. The submitter assumes that they are somewhere in the `/store/group/` space, but you have to specify where
+ `-d` is an imperfect accounting mechanism for nameing the output folder. It takes any string, it chose it to be a date or something. *IMPORTANT NOTE:* by default this trimmer outputs to the `lpcboostres` group space, so if you do not have write access, please edit the output skim path prior to submission to reflect this.
+ `-c` is the chuck size, or how many ntuples files to string together at a time as you skim. 20 is always safe, for data you can go up to 50, but that gets risky for DY+jets samples. The scripts will work, but you get Zombie files at output. 

An example submission is:

```bash
python submitTrimmerToCondor.py -s samplesToSkim_2018_DYJetsToLL_M-50_HT-800to1200.txt -e lpcboostres/dyjets2018_feb2021 -d Feb2021 -c 20
```

The you can monitor and check you jobs with the standard `condor_q` and whatnot.

##Common pitfalls and built-in checks

The most common failure mode is the `xrdcp` step. That is mostly mitigated with the list of preferred sites, but it can still crop up. A good feature request would be to hold the job, but in our case the job just ends in failure. To check and resubmit, from the main `trimmerShed` directory

```bash
source checkAndResubXrdcpErrors.sh
```

The `countOutput.py` script is only meant for checking complete ntuple submissions on LPC Condor, so it currently does not work for CMS Connect. Can be made more robust, and does not pertain to the trimmer.

The other `.sh` scripts are meant for batch copying from the `cmseos.fnal.gov` space to `cmslpc`, and must be exectued from `cmslpc` machines.


