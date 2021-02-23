#!/bin/bash

for i in `eosls /store/group/lpcboostres/$1 | grep $3`
do
    xrdcp root://cmseos.fnal.gov//store/group/lpcboostres/$1/$i root://cmseos.fnal.gov//store/group/lpcboostres/$2/$i
done
