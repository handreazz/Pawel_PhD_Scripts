#!/bin/bash

if [ -e Frames.m ] ; then
  rm Frames.m
fi

I=0
NFRM=1
while [ ${I} -le 15 ] ; do
  echo "T(:,:,${NFRM}) = [" >> Frames.m
  if [ -e md${I}.rst ] ; then
    head -50 md${I}.rst | tail -48 >> Frames.m
  else
    head -50 /home/case/xtal/fav8/fav8/md${I}.rst | tail -48 >> Frames.m
  fi  
  echo "];" >> Frames.m
  let "NFRM+=1"
  let "I+=1"
done

