#! /bin/bash


echo "Average structure backbone rmsds" >summary.txt
echo -e 'structure(ns)  \t  rmsd' >>summary.txt

for i in `ls avg_rmsd_bbone*`;do 
	j=${i##*bbone_}
	j=${j%.dat}
	rmsd=`cat $i | awk '{print $2'}`
	printf "%3s \t\t  %6.4f\n" "$j"  "$rmsd" >>summary.txt
done

echo -e "\n\nAverage structure side chain rmsds" >>summary.txt
echo -e 'structure(ns)  \t  rmsd' >>summary.txt
for i in `ls avg_rmsd_sdcn*`;do 
	j=${i##*sdcn_}
	j=${j%.dat}
	rmsd=`cat $i | awk '{print $2'}`
	printf "%3s \t\t  %6.4f\n" "$j"  "$rmsd" >>summary.txt
done
