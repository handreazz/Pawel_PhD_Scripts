#! /bin/bash 


#convert to fractional
  coordconv xyzin vs_sim_mod.pdb xyzout new1.xyz << EOF >/dev/null
INPUT PDB
OUTPUT FRAC
END
EOF

# only shift the second monomer (last 66 line) by c=-1  
# first monomer stays the same
head -66 new1.xyz >new2.xyz


  tail -66 new1.xyz |\
  awk '{fa=$2;\
        fb=$3;\
        fc=$4-1;\
   printf("%5d%10.5f%10.5f%10.5f%s\n",\
      $1,fa,fb,fc,substr($0,36))}' |\
  cat > new3.xyz

cat new2.xyz new3.xyz >new4.xyz

#convert back to pdb
  coordconv xyzin new4.xyz xyzout sfallme.pdb << EOF > /dev/null
CELL 10.802   16.361   17.853 116.40  95.54  93.16
INPUT FRAC
OUTPUT PDB
END
EOF


