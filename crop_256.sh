#!/bin/bash

for entry in "out_cropped_256"/*
do
  gm convert -size 512x512 $entry -thumbnail 256x256^ -gravity center -extent 256x256 +profile "*" $entry
  echo "$entry"
done
