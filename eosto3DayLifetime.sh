#!/bin/bash

for i in `eosls /store/group/lpcboostres/$1`
do
    xrdcp root://cmseos.fnal.gov//store/group/lpcboostres/$1/$i /uscmst1b_scratch/lpc1/3DayLifetime/gcumming/$1/$i
done
