#!/bin/bash
 for i in `seq 0 360`; do
   echo -n "$i, "
   DIR=scan_step$i
   if [ $i -lt 100 ]; then DIR=scan_step0$i; fi
   if [ $i -lt 10 ]; then DIR=scan_step00$i; fi
   if [ ! -d $DIR ]; then mkdir $DIR; fi
   cp CAC_dihEric.com $DIR.com
   j=$(echo "scale=4; 2.00*$i" | bc)
   x=$(echo "scale=4; 120.00 + $j" | bc)
   y=$(echo "scale=4; 240.00 + $j" | bc)

	
   sed -i s/"XXXXXXXXXX"/$j/ $DIR.com
   sed -i s/"YYYYYYYYYY"/$x/ $DIR.com
   sed -i s/"ZZZZZZZZZZ"/$y/ $DIR.com
   sed -i s/CHECK/$DIR/      $DIR.com
   mv $DIR.com $DIR
 done
echo Done
