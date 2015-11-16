sf-valid is here
  svn co https://svn-dev.wwpdb.org/svn-test/sf/sf-valid/trunk sf-valid

AFITT
dcc -pdb 1cvu_sc_10_adp__001.pdb -sf 1cvu_10refined_001.mtz -lldf
                        rscc    rsr     rsrz
1    ? A ACD  701 . .   0.957  0.118    0.01    29.04  1.000
1    ? B ACD 2701 . .   0.965  0.127    0.16    29.41  1.000

EH
dcc -pdb 1cvu_no_afitt___001.pdb -sf 1cvu_10refined_001.mtz -lldf
1    ? A ACD  701 . .   0.958  0.112   -0.10    28.85  1.000 
1    ? B ACD 2701 . .   0.972  0.114   -0.07    28.99  1.000 

10REFINED EH
dcc -pdb 1cvu_10refined_001.pdb -sf 1cvu_10refined_001.mtz -lldf
1    ? A ACD  701 . .   0.958  0.112   -0.10    28.85  1.000 
1    ? B ACD 2701 . .   0.972  0.114   -0.07    28.99  1.000 

START
dcc -pdb ../1cvu_oe.pdb -sf 1cvu_10refined_001.mtz -lldf
1 xxxx A ACD  701 . .   0.928  0.179    0.54    23.86  1.000 
1 xxxx B ACD 2701 . .   0.957  0.225    1.44    25.20  1.000 

                               rscc
AFITT
phenix.real_space_correlation 1cvu_sc_10_adp__001.pdb 1cvu_10refined_001.mtz detail=residue | grep ACD
 A   ACD  701   1.00   29.04  0.9618   2.61   2.42
 B   ACD 2701   1.00   29.41  0.9619   2.47   2.38

EH
phenix.real_space_correlation 1cvu_no_afitt___001.pdb 1cvu_10refined_001.mtz detail=residue | grep ACD
 A   ACD  701   1.00   28.85  0.9641   2.66   2.48
 B   ACD 2701   1.00   28.99  0.9645   2.52   2.43

10REFINED EH
phenix.real_space_correlation 1cvu_10refined_001.pdb  1cvu_10refined_001.mtz detail=residue | grep ACD
 A   ACD  701   1.00   28.68  0.9647   2.66   2.46
 B   ACD 2701   1.00   28.73  0.9645   2.52   2.42

START
phenix.real_space_correlation ../1cvu_oe.pdb  1cvu_10refined_001.mtz detail=residue | grep ACD
 A   ACD  701   1.00   23.86  0.9413   2.38   2.31
 B   ACD 2701   1.00   25.20  0.9232   2.20   2.22



