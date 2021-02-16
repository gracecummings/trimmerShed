#!/bin/bash

for i in `ls condorTrimmerOutput/$1/ | grep .stdout`
do 
if [[ $(tail condorTrimmerOutput/$1/$i) == *failure* ]]; then
    echo "Found a failure in xrdcp for "${i%_out.stdout}
    #echo trimmer_${i%_out.stdout}_$1.jdl
    condor_submit trimmer_${i%_out.stdout}_$1.jdl
fi
done
echo "End of xrdcp check, if no failures reported, none were found."
