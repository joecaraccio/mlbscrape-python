#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pwd
cd $DIR
output_filename=$DIR/logs/"mine_pregame"_$(date +%F)".txt"
echo $output_filename

python $DIR/mine_pregame.py >> $output_filename