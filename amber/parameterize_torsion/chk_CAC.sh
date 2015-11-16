#!/bin/bash
        for i in */;
        do
                cd $i

		k=$(grep " Normal termination of Gaussian 03" *.out)
		if [ -n "$k" ]; then
			echo "Something is Afoot with" *.out
		fi

		y=`grep "SCF Done:  E(RB3LYP)" *.out | tail -1`
		y=${y##???????????????????????}
		y=${y%???????????????????????}
		y=$(echo "scale=4; 630.0*$y" | bc)

		z=`ls *out`
		z=${z##scan_step}
		z=${z%.out}
		z=$(echo "scale=4; 2.00*$z" | bc)

		echo -e ${z} "\t" ${y}
		cd ../

        done
