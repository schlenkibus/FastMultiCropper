#!/bin/bash

for entry in "out_padded"/*
do
  convert $entry -resize 256x256 -gravity center -background "rgb(0,0,0)" -extent 256x256 +profile "*" $entry
  echo "$entry"
done
