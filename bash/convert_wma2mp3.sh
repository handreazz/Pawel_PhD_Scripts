#! /bin/bash

for i in *.wma
do    
MN=`basename "$i" .wma`.mp3
mplayer -vo null -vc null -af resample=44100 -ao pcm:waveheader "$i" && lame -m s audiodump.wav -o "$MN"
done

