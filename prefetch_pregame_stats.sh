#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pwd
cd $DIR
output_filename=$DIR/logs/"prefetch"_$(date +%F)".txt"
echo $output_filename

python $DIR/prefetch_pregame_stats.py >> $output_filename