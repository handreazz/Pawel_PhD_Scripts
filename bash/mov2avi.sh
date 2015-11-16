#! /bin/bash
#~ #IFS=$'\n'

#~ for i in *.MOV;
#~ do
#~ name=`echo ${i%.MOV}`
#~ echo $name;
#~ avconv -i ${name}.MOV -b 19000k -b:a 192k -s 960x540 ${name}.avi
#~ done



#~ 
#~ for i in *.MPG;
#~ do
#~ name=`echo ${i%.MPG}`
#~ echo $name;
#~ avconv -i ${name}.MPG -b 19000k -b:a 192k -s 960x540 ${name}.avi
#~ done


for i in *.avi;
do
name=`echo ${i%.avi}`
echo $name;
avconv -i ${name}.avi -b 19000k -b:a 192k -s 960x540 ${name}.MPG
done
