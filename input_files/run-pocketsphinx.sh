#!/bin/bash

pocketsphinx_continuous \
    -hmm model_parameters/voxforge.cd_cont_4000 \
    -lw 10 -feat 1s_c_d_dd -beam 1e-80 -wbeam 1e-40 \
    -dict /home/ai/voxforge/de/work/etc/voxforge.dic \
    -lm /home/ai/voxforge/de/work/etc/voxforge.lm.DMP \
    -wip 0.2 \
    -agc none -varnorm no -cmn current


