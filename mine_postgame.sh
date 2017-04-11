#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pwd
cd $DIR
output_filename=$DIR/logs/"mine_postgame"_$(date +%F)".txt"
echo $output_filename

python $DIR/mine_postgame.py >> $output_filename