#!/bin/csh -f
echo "Demo run of calculation of structure factors from MD data"
echo "Getting structure factors from all models in one file:"
phenix.python $PHENIX/phenix/phenix/utilities/get_struct_fact_from_md.py \
  pdb_file=md_0_1_prot_demo_1.pdb solvent_file=md_0_1_solv_demo_1.pdb \
  n_skip=0 \
  d_min=2.2 \
  output_prefix=md_0_1_prot_solv_demo_1 \
  include_h=1 

echo "Merging structure factors from all files:"
phenix.python $PHENIX/phenix/phenix/utilities/get_struct_fact_from_md.py \
   template=md_0_1_prot_solv_demo \
   first=1 last=1 \
   merge=true

