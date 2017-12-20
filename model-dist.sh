#!/bin/bash

datum=`date +%Y%m%d`

rm -rf models-dist
mkdir models-dist

pushd models
MODEL='de_3_512'
tar cfv ../models-dist/${MODEL}_${datum}.tar ${MODEL} ${MODEL}.ini
xz -v -8 -T 4 ../models-dist/${MODEL}_${datum}.tar
MODEL='en_3_512'
tar cfv ../models-dist/${MODEL}_${datum}.tar ${MODEL} ${MODEL}.ini
xz -v -8 -T 4 ../models-dist/${MODEL}_${datum}.tar
popd

echo rsync -avPz --delete --bwlimit=256 models-dist/ goofy:/var/www/html/zamia-ai/

