#!/bin/bash

cd /home/ai/voxforge/de

pushd audio-arc

wget -c -r -nd -l 1 -np http://www.repository.voxforge1.org/downloads/de/Trunk/Audio/Main/16kHz_16bit/

popd

pushd audio
for i in ../audio-arc/*.tgz ; do

    echo $i

    tar xfz $i

done

popd

