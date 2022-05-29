#!/bin/bash

for entry in "out_more_cleaner_512_2"/*
do
  echo $entry
  useImage=0
  for dimension in $(identify $entry | awk '{print $3}' | tr "x" "\n")
  do
  	if [ $dimension -gt 349 ]; then
		useImage=1
	fi
  done
  if [ $useImage -eq 1 ]; then
    convert $entry -resize 512x512 -gravity center -background "rgb(0,0,0)" -extent 512x512 +profile "*" $entry
  else
    rm $entry
  fi
done
