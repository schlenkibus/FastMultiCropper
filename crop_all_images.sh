#!/bin/bash

for entry in "out_cropped"/*
do
  gm convert -size 256x256 $entry -thumbnail 128x128^ -gravity center -extent 128x128 +profile "*" $entry
  echo "$entry"
done
