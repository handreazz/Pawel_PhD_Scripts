#! /bin/bash

#make sure to edit sandbox.py
for i in `seq 1 9`
do
echo $i
~/c/Case/contacts/sandbox.py PDBData/000$i.pdb >residueContacts/000$i.dat
done


for i in `seq 10 99`
do
echo $i
~/c/Case/contacts/sandbox.py PDBData/00$i.pdb >residueContacts/00$i.dat
done

for i in `seq 100 110`
do
echo $i
~/c/Case/contacts/sandbox.py PDBData/0$i.pdb >residueContacts/0$i.dat
done
