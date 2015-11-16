#! /bin/bash

Bres_no1=600
Eres_no1=601

#james holton way
echo "VERSION 1"
cat <<EOF > awk.in
BEGIN{bres=$Bres_no1; eres=$Eres_no1;}
/ATOM/{RES= substr(\$0, 23, 4); CHAIN=substr(\$0, 22,1); if (CHAIN=="A" && RES+0>=bres && RES+0<=eres) print \$0;}
EOF
awk -f awk.in out1.pdb 

#better: use -v
echo "VERSION 2"
cat <<EOF > awk.in
/ATOM/{RES= substr(\$0, 23, 4); CHAIN=substr(\$0, 22,1); if (CHAIN=="A" && RES+0>=bres && RES+0<=eres) print \$0;}
EOF
awk -v bres="$Bres_no1" -v eres="$Eres_no1" -f awk.in out1.pdb

#james holton way command line: need to escape the quotes and awk variables,  
#but use double quotes so that shell variables get expanded
echo "VERSION 3"
awk "BEGIN{bres=$Bres_no1; eres=$Eres_no1;} \
     {RES= substr(\$0, 23, 4); CHAIN=substr(\$0, 22,1); \
     if (CHAIN==\"A\" && RES+0>=bres && RES+0<=eres) print \$0;}" out1.pdb

#better command line way (-v)
echo "VERSION 4"
awk -v bres="$Bres_no1" -v eres="$Eres_no1" '/ATOM/{if                  \
  (substr($0,23,4)+0>=bres && substr($0,23,4)+0<=eres && substr($0,22,1)=="A") \
   print $0}' out1.pdb
